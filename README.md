# Inventory Management System

A simple, intuitive inventory management tool designed for offline businesses to easily record and track products sold to customers. Built with Flask, SQLite, and a clean, responsive web interface.

## Features

### 🎯 Core Features
- **Product Management**: Add, edit, and delete products with detailed information
- **Sales Tracking**: Record sales transactions with automatic stock updates
- **Stock Management**: Monitor stock levels with low stock alerts
- **Dashboard**: Real-time overview of key business metrics
- **Reports**: Generate business insights and sales analytics
- **Offline-First**: Works completely offline with local SQLite database

### 📊 Dashboard Highlights
- Total products, sales, and revenue at a glance
- Low stock alerts for inventory management
- Top-selling products analysis
- Recent sales activity
- Quick action buttons for common tasks

### 🛍️ Sales Features
- Easy sale recording with product selection
- Automatic stock deduction
- Customer name tracking (optional)
- Real-time total calculation
- Stock availability validation

### 📈 Reporting & Analytics
- 30-day sales and revenue metrics
- Top-performing products
- Business insights and recommendations
- Printable reports
- Sales history tracking

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (lightweight, no setup required)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-friendly interface

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Start managing your inventory!

### First Time Setup
- The application will automatically create the database on first run
- No additional configuration required
- Start by adding your first product

## 🚀 Railway Deployment (Recommended)

This application is now configured for easy deployment on Railway!

### Quick Deploy
1. **Push code to GitHub**
2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
3. **Add PostgreSQL database** in Railway dashboard
4. **Set environment variables**:
   - `SECRET_KEY`: A secure secret key

### Generate Secret Key
```bash
python deploy.py
```

### Detailed Instructions
See [railway-deploy.md](railway-deploy.md) for complete deployment guide.

## 🚀 Alternative Deployment Options

See [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md) for multiple deployment platforms:
- Railway (Recommended)
- Render
- Heroku
- PythonAnywhere
- DigitalOcean

## Usage Guide

### Getting Started
1. **Add Products**: Go to "Products" → "Add Product" to add your inventory items
2. **Record Sales**: Use "Sales" → "Record Sale" to track customer transactions
3. **Monitor Dashboard**: Check the main dashboard for business overview
4. **Generate Reports**: Visit "Reports" for detailed analytics

### Product Management
- **Add Product**: Include name, description, price, cost, and initial stock
- **Edit Product**: Update information and stock levels as needed
- **Delete Product**: Remove products from inventory (use with caution)
- **Stock Alerts**: Automatic warnings when stock falls below minimum levels

### Sales Recording
- **Select Product**: Choose from available products with stock
- **Enter Quantity**: Specify number of units sold
- **Customer Info**: Optional customer name for tracking
- **Automatic Updates**: Stock levels update automatically after sale

### Dashboard Features
- **Key Metrics**: View total products, sales, revenue, and low stock items
- **Quick Actions**: Fast access to common tasks
- **Recent Activity**: Latest sales and stock updates
- **Alerts**: Low stock warnings and business insights

## File Structure

```
inventory-management-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── dashboard.html    # Main dashboard
│   ├── products.html     # Product listing
│   ├── add_product.html  # Add product form
│   ├── edit_product.html # Edit product form
│   ├── sales.html        # Sales history
│   ├── add_sale.html     # Record sale form
│   └── reports.html      # Business reports
└── inventory.db          # SQLite database (created automatically)
```

## Database Schema

### Products Table
- `id`: Primary key
- `name`: Product name
- `description`: Product description
- `price`: Selling price
- `cost`: Cost price
- `stock_quantity`: Current stock level
- `min_stock_level`: Minimum stock alert threshold
- `category`: Product category
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Sales Table
- `id`: Primary key
- `product_id`: Foreign key to products
- `quantity`: Units sold
- `total_amount`: Total sale amount
- `customer_name`: Customer name (optional)
- `sale_date`: Sale timestamp

## Customization

### Adding Categories
Edit the category options in:
- `templates/add_product.html`
- `templates/edit_product.html`
- `templates/products.html`

### Styling
Modify the CSS in `templates/base.html` to customize the appearance.

### Features
Extend functionality by adding new routes in `app.py` and corresponding templates.

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database issues**
```bash
# Delete inventory.db and restart the application
rm inventory.db
python app.py
```

**Import errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### Support
- Check that Python 3.7+ is installed
- Verify all dependencies are installed correctly
- Ensure the application has write permissions for the database file

## Security Notes

- This is a local application designed for offline use
- No user authentication is implemented
- Database file should be backed up regularly
- Consider adding authentication for multi-user environments

## Future Enhancements

Potential features for future versions:
- User authentication and roles
- Barcode scanning support
- Export functionality (CSV, PDF)
- Advanced reporting and charts
- Backup and restore functionality
- Multi-location support
- Email notifications for low stock

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Built with ❤️ for small businesses who need simple, effective inventory management.** 