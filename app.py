from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Use PostgreSQL on Railway, fallback to SQLite for local development
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # Add PostgreSQL specific configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
else:
    # For local development, use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=5)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    customer_name = db.Column(db.String(100))
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref='sales')

# Initialize database
def init_db():
    with app.app_context():
        try:
            db.create_all()
            # Add some sample data if database is empty
            if Product.query.count() == 0:
                sample_products = [
                    Product(name='Sample Product 1', description='A sample product', 
                           price=100.0, cost=60.0, stock_quantity=50, category='Electronics'),
                    Product(name='Sample Product 2', description='Another sample product', 
                           price=200.0, cost=120.0, stock_quantity=30, category='Clothing'),
                ]
                for product in sample_products:
                    db.session.add(product)
                db.session.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")

# Routes
@app.route('/')
def dashboard():
    try:
        # Get dashboard statistics
        total_products = Product.query.count()
        total_sales = Sale.query.count()
        
        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Sale.total_amount)).scalar() or 0
        
        # Calculate total profit
        total_profit = db.session.query(db.func.sum((Product.price - Product.cost) * Sale.quantity)).join(Product, Product.id == Sale.product_id).scalar() or 0
        
        # Get low stock products
        low_stock_products = Product.query.filter(Product.stock_quantity <= Product.min_stock_level).all()
        
        # Get top selling products
        top_products = db.session.query(
            Product.name,
            db.func.sum(Sale.quantity).label('total_sold'),
            db.func.sum(Sale.total_amount).label('total_revenue')
        ).join(Sale).group_by(Product.id).order_by(db.func.sum(Sale.quantity).desc()).limit(5).all()
        
        # Get recent sales
        recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()
        
        return render_template('dashboard.html',
                             total_products=total_products,
                             total_sales=total_sales,
                             total_revenue=total_revenue,
                             total_profit=total_profit,
                             low_stock_products=low_stock_products,
                             top_products=top_products,
                             recent_sales=recent_sales)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html',
                             total_products=0,
                             total_sales=0,
                             total_revenue=0,
                             total_profit=0,
                             low_stock_products=[],
                             top_products=[],
                             recent_sales=[])

@app.route('/products')
def products():
    try:
        products = Product.query.order_by(Product.name).all()
        return render_template('products.html', products=products)
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'error')
        return render_template('products.html', products=[])

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            cost = float(request.form['cost'])
            stock_quantity = int(request.form['stock_quantity'])
            min_stock_level = int(request.form['min_stock_level'])
            category = request.form['category']
            
            product = Product(
                name=name,
                description=description,
                price=price,
                cost=cost,
                stock_quantity=stock_quantity,
                min_stock_level=min_stock_level,
                category=category
            )
            
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
            return redirect(url_for('add_product'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    try:
        product = Product.query.get_or_404(id)
        
        if request.method == 'POST':
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.cost = float(request.form['cost'])
            product.stock_quantity = int(request.form['stock_quantity'])
            product.min_stock_level = int(request.form['min_stock_level'])
            product.category = request.form['category']
            
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        
        return render_template('edit_product.html', product=product)
    except Exception as e:
        flash(f'Error editing product: {str(e)}', 'error')
        return redirect(url_for('products'))

@app.route('/products/delete/<int:id>')
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    try:
        sales = Sale.query.order_by(Sale.sale_date.desc()).all()
        return render_template('sales.html', sales=sales)
    except Exception as e:
        flash(f'Error loading sales: {str(e)}', 'error')
        return render_template('sales.html', sales=[])

@app.route('/sales/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
            customer_name = request.form['customer_name']
            action = request.form.get('action', 'record')
            unit_price = float(request.form.get('unit_price', 0))
            
            product = Product.query.get_or_404(product_id)
            
            if product.stock_quantity < quantity:
                flash('Insufficient stock!', 'error')
                return redirect(url_for('add_sale'))
            
            total_amount = unit_price * quantity
            
            sale = Sale(
                product_id=product_id,
                quantity=quantity,
                total_amount=total_amount,
                customer_name=customer_name
            )
            
            # Update stock
            product.stock_quantity -= quantity
            
            db.session.add(sale)
            db.session.commit()
            
            if action == 'print_record':
                return redirect(url_for('print_receipt', sale_id=sale.id))
            else:
                flash('Sale recorded successfully!', 'success')
                return redirect(url_for('sales'))
        except Exception as e:
            flash(f'Error recording sale: {str(e)}', 'error')
            return redirect(url_for('add_sale'))
    
    try:
        products = Product.query.filter(Product.stock_quantity > 0).order_by(Product.name).all()
        return render_template('add_sale.html', products=products)
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'error')
        return render_template('add_sale.html', products=[])

@app.route('/reports')
def reports():
    try:
        # Sales report for last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_sales = Sale.query.filter(Sale.sale_date >= thirty_days_ago).all()
        
        # Calculate metrics
        total_sales_30d = len(recent_sales)
        total_revenue_30d = sum(sale.total_amount for sale in recent_sales)
        # Calculate total profit for last 30 days
        total_profit_30d = sum((sale.product.price - sale.product.cost) * sale.quantity for sale in recent_sales)
        
        # Top selling products
        top_products = db.session.query(
            Product.name,
            db.func.sum(Sale.quantity).label('total_sold'),
            db.func.sum(Sale.total_amount).label('total_revenue')
        ).join(Sale).group_by(Product.id).order_by(db.func.sum(Sale.quantity).desc()).all()
        
        return render_template('reports.html',
                             total_sales_30d=total_sales_30d,
                             total_revenue_30d=total_revenue_30d,
                             total_profit_30d=total_profit_30d,
                             top_products=top_products,
                             recent_sales=recent_sales)
    except Exception as e:
        flash(f'Error loading reports: {str(e)}', 'error')
        return render_template('reports.html',
                             total_sales_30d=0,
                             total_revenue_30d=0,
                             total_profit_30d=0,
                             top_products=[],
                             recent_sales=[])

@app.route('/api/products')
def api_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'stock_quantity': p.stock_quantity
        } for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sale/<int:sale_id>')
def api_sale_detail(sale_id):
    try:
        sale = Sale.query.get_or_404(sale_id)
        return jsonify({
            'id': sale.id,
            'product_name': sale.product.name,
            'unit_price': sale.product.price,
            'quantity': sale.quantity,
            'total_amount': sale.total_amount,
            'customer_name': sale.customer_name,
            'sale_date': sale.sale_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a new route for printing the receipt
def format_currency(amount):
    return f"₹{amount:,.2f}"

@app.route('/sales/receipt/<int:sale_id>')
def print_receipt(sale_id):
    try:
        sale = Sale.query.get_or_404(sale_id)
        return render_template('receipt.html', sale=sale, format_currency=format_currency)
    except Exception as e:
        flash(f'Error loading receipt: {str(e)}', 'error')
        return redirect(url_for('sales'))

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Inventory system is running'})

# Initialize database when app starts
init_db()

# For Railway deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
