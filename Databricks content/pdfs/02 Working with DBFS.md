Databricks DBFS Overview
• DBFS = Databricks File System
• Distributed filesystem accessible from all
clusters
• Backed by cloud storage (S3, ADLS, GCS)
• Uniform path format: dbfs:/
• Used for datasets, libraries, checkpoints
• Supports Delta Lake, Parquet, CSV, JSON
DBFS Path Types
• dbfs:/ – virtual filesystem root
• /FileStore – web-accessible uploads
• /mnt – mounted cloud storage
locations
• dbfs:/databricks-datasets – sample
datasets
• Local ephemeral storage on
driver/node
• Cloud object storage integration
List Directories
• List directory contents:
• `dbutils.fs.ls("dbfs:/")`
• Shows files, types, sizes
• Supports nested paths
• Used for exploration and verification
• Works across all clusters
Create Directories
• Create new folder in DBFS:
• `dbutils.fs.mkdirs("dbfs:/lab/data")`
• Creates intermediate directories if missing
• Useful for ETL workflows
• Organizes pipeline outputs
• Helps structure notebooks and jobs
Upload Data to DBFS
• Upload via UI: Data → DBFS → Upload
• Upload via CLI: `databricks fs cp`
• Upload via REST API for automation
• Notebook upload: `dbutils.fs.cp`
• FileStore supports web downloads
• Data becomes accessible across notebooks
Copy Files
• Copy command syntax:
• `dbutils.fs.cp(src, dst)`
• Example:
• `dbutils.fs.cp("dbfs:/src.txt", "dbfs:/backup/src.txt")`
• Use for backup, migration, ETL steps
• Works across mounted storage
Move / Rename Files
• Move command:
• `dbutils.fs.mv(src, dst)`
• Example:
• `dbutils.fs.mv("dbfs:/tmp/a.csv", "dbfs:/archive/a.csv")`
• Useful for archiving
• Ensures clean directory structure
Delete Files & Folders
• Delete single file:
• `dbutils.fs.rm("dbfs:/tmp/a.csv")`
• Recursive delete:
• `dbutils.fs.rm("dbfs:/tmp", True)`
• Used for cleanup tasks
• Supports automation in jobs
Read Data (Spark API)
• CSV read:
• `spark.read.csv(path, header=True)`
• JSON read:
• `spark.read.json(path)`
• Parquet read:
• `spark.read.parquet(path)`
• Delta read:
• `spark.read.format("delta").load(path)`
• DBFS works seamlessly with all formats
Write Data (Spark API)
• Write CSV:
• `df.write.csv(path)`
• Write JSON:
• `df.write.json(path)`
• Write Parquet:
• `df.write.parquet(path)`
• Write Delta:
• `df.write.format("delta").save(path)`
• Support overwrite mode
DBFS Utilities
• Check existence via `dbutils.fs.ls`
• Preview file: `dbutils.fs.head(path)`
• Tail file: `dbutils.fs.tail(path)`
• Supports fast debugging
• Useful for ETL pipelines
• Built for interactive exploration
Mounting Cloud Storage
• Mount ADLS/S3 to DBFS
• `dbutils.fs.mount()`
• Mounts appear under /mnt
• Requires service principal or keys
• Unified path for batch/ML workflows
• Preferred in enterprise environments
DBFS in Jobs
• Jobs read/write to DBFS
• Checkpoints stored in DBFS
• Used for ETL orchestration
• Job clusters clean temp storage
• Supports DAG-style workflows
• Reliable for production pipelines
DBFS Best Practices
• Organize by project and data stage
• Use Delta Lake as default format
• Avoid storing large files in FileStore
• Use mounts for production storage
• Clean unused checkpoint folders
• Enable Unity Catalog for governance
Summary of DBFS Commands
• dbutils.fs.ls – list directories
• dbutils.fs.mkdirs – create
• dbutils.fs.cp – copy files
• dbutils.fs.mv – move/rename
• dbutils.fs.rm – delete files
• Spark APIs for read/write operations