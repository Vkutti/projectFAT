from cs50 import SQL

# Connect to the database
db = SQL("sqlite:///FAT.db")

# Step 1: Rename the existing table
db.execute("ALTER TABLE fat RENAME TO fat_backup;")

# Step 2: Create a new table with the id column as AUTOINCREMENT
db.execute("""
    CREATE TABLE fat (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        businessName TEXT NOT NULL,
        ownername TEXT NOT NULL,
        businessType TEXT NOT NULL,
        businessHours TEXT NOT NULL,
        businessLocation TEXT NOT NULL
    );
""")

# Step 3: Copy data from the old table to the new table
db.execute("""
    INSERT INTO fat (id, businessName, ownername, businessType, businessHours, businessLocation)
    SELECT id, businessName, ownername, businessType, businessHours, businessLocation
    FROM fat_backup;
""")

# Step 4: Drop the old table
db.execute("DROP TABLE fat_backup;")

print("id column has been successfully updated to AUTOINCREMENT.")
