
# Data files location
DATA_DIR = "data/"
RAW_SALES = "ExportSalesData_3_0_stripped.csv"
SALES = "sales.csv"
RAW_INVENTORY = "merged_stocks.csv"
INVENTORY = "inventory.csv"
RAW_ITEMS = "ExportItemData_2_0_stripped.csv"
SALES_COLUMNS_SELECTION = "sales_columns_selection.txt"

# Smallest granularity
# one of D, W, M, Q, Y
SAMPLING = "D"

# Size column
SIZE_COLUMN = "Horizontal Component Code"

# Default dates for dropdowns
# TODO: Set date selector in layout_.py with these defaults
START_DATE, END_DATE = "2015-08-01", "2017-12-31"  # dt.date(2015, 8, 1), dt.date(2017, 12, 31)

# Filters
# TODO: Modify FILTERS to be a dict with keys inventory & sales, corresponding to
# TODO: filters in inventory & sales data and the elements of the selection for the dashboard
# TODO: Careful: some operations that use the variable must be modified
# TODO: Migrate ipywidget filters to dash
FILTERS = [

    # eg: (column name, display name, default value)
    ("Web Shop Code", "Retailer", None),
    ("Merchandise Code", "Category", None),
    ("Brand", "Brand", "EKS"),
    ("Season", "Season", None),
    # ("Item No_", "Item Number"),
    # ("External Record Id", "Product ID")

]