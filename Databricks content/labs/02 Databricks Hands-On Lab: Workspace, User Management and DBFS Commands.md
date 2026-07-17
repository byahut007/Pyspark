Databricks Hands-On Lab: Workspace, User Management & DBFS Commands

Platform: Databricks Community Edition + Azure Databricks
Duration: 60–70 minutes


Lab Objectives


By the end of this lab, learners will:

Understand Databricks workspace components (notebooks, repos, clusters, jobs).
Execute DBFS operations using dbutils.fs and Spark DataFrame reads/writes.
Explore user management features (Community Edition vs Azure Databricks).
Run Python, SQL, Scala commands in notebooks.
Learn best practices for workspace organization and governance.

Lab Prerequisites
For Databricks Community Edition
Free account at: https://community.cloud.databricks.com
No Azure subscription needed.
For Azure Databricks
Azure Subscription
Owner/Contributor rights to create resources
Azure AD access to add users (optional for User Management section)
----------------------------
SECTION 1 — Create a Databricks Workspace
----------------------------

Part A — Databricks Community Edition Workspace (10 mins)
Step 1 — Sign up
Open: https://community.cloud.databricks.com
Click Sign Up → enter email → verify OTP.
Create account and wait for workspace deployment.
Step 2 — Understanding the Landing Page
After login, locate:

Compute – default community cluster
Workspace – notebooks and folders
Repos – Git-based versioning
Data – tables, databases, DBFS browser
Jobs – automation section (limited in CE)
Step 3 — Create Your First Folder
In Workspace → Users → your_email:

Click Create → Folder
Name it: lab_databricks_introduction
This is your own sandbox.



Step 4 — Create a Notebook
Right-click folder → Create → Notebook
Name: dbfs_lab_notebook
Default language: Python

Part B — Azure Databricks Workspace (15 mins)
Step 1 — Create Azure Databricks Workspace
Portal → Create a Resource
Search Azure Databricks
Fill:
Subscription
Resource Group
Workspace Name
Region: East US
Pricing Tier: Premium (recommended)
Click Review + Create
Step 2 — Explore Azure Databricks Resource Blade
Open the newly deployed workspace:

You will see:

Overview
Managed Resource Group
Networking
Monitoring
Access Control (IAM)
Step 3 — Launch Workspace
Click Launch Workspace → You enter the Databricks UI.

Identify:

Compute
Workspace
Repos
Data
SQL Editor
Admin Console (only in Azure)
----------------------------
SECTION 2 — User Management (Azure Only)
----------------------------
Step 1 — Open Admin Console
Top right → User Icon → Admin Console
You will see tabs:

Users
Groups
Service Principals
Workspace Settings
SCIM
Audit Logs
Step 2 — Add a User
Go to Users
Click Add User
Enter email: test.user@yourorg.com
Assign User role
👉 Community Edition does NOT support multi-user management.



Step 3 — Assign Admin Role
Select user
Click Assign Admin
Validate admin badge appears
Step 4 — Add a Service Principal
(For CI/CD automation)

Go to Service Principals
Click Add
Enter App registration details
Assign access to clusters/jobs
Verification Task
✔ Add one user with admin role

✔ Create another user with cluster access only

✔ Create a service principal

----------------------------
SECTION 3 — Compute Setup (Both Platforms)
----------------------------
Step 1 — Create a Cluster
Go to Compute → Create Cluster
Enter:
Name: lab_cluster
Runtime: 13.x (or latest)
Worker Type: Small (Standard_DS3_v2 in Azure)
Workers: 1–2
Enable Auto-termination = 15 mins
Start the cluster.



----------------------------
SECTION 4 — DBFS Hands-On (Core Lab)
----------------------------
Open your notebook created earlier. Attach the cluster.


Task 1 — Explore DBFS
Step 1 — List root directories
dbutils.fs.ls("dbfs:/")
Expected items:

FileStore
user
databricks-datasets (Azure only)
Step 2 — Explore FileStore
dbutils.fs.ls("dbfs:/FileStore")
FileStore is web-accessible.


Task 2 — Upload Files to DBFS
Method A — Using UI
Go to Data → DBFS
Click Upload File
Upload a sample CSV (e.g., people.csv)
File path becomes:

/FileStore/tables/people.csv
Method B — Using CLI (Azure Only)
Install CLI:

pip install databricks-cli
Login:

databricks configure --token
Upload:

databricks fs cp localfile.csv dbfs:/FileStore/localfile.csv

Task 3 — Read File with Spark
df = spark.read.csv("dbfs:/FileStore/tables/people.csv", header=True, inferSchema=True)
df.show()
Add tasks:

Count
Select
Filter
Example:

df.count()
df.filter("age > 30").show()
df.select("name").show()

Task 4 — Create a Directory in DBFS
dbutils.fs.mkdirs("dbfs:/lab/output")

Task 5 — Write Data to DBFS
df.write.mode("overwrite").json("dbfs:/lab/output/json_data")
Verify:

dbutils.fs.ls("dbfs:/lab/output/json_data")

Task 6 — Copy Files in DBFS
dbutils.fs.cp("dbfs:/FileStore/tables/people.csv", "dbfs:/lab/people_copy.csv")

Task 7 — Remove Files
dbutils.fs.rm("dbfs:/lab/people_copy.csv")
----------------------------
SECTION 5 — Notebook Multi-Language Execution
----------------------------
Run Python
print("Hello from Python")
Run SQL
%sql
SELECT "Hello from SQL"
Run Scala
%scala
println("Hello from Scala")
Run Markdown
%md
# This is a markdown cell
----------------------------
SECTION 6 — Optional: Unity Catalog Exploration (Azure Only)
----------------------------
If Unity Catalog is enabled:

List Catalogs
%sql
SHOW CATALOGS;
List Schemas
%sql
SHOW SCHEMAS IN main;
Create External Table
CREATE TABLE main.default.people (
  name STRING,
  age INT
)
USING CSV
LOCATION 'abfss://<container>@<storage>.dfs.core.windows.net/people.csv';


SECTION 8 — Lab Conclusion
Learners now understand:

Databricks workspace navigation
Multi-language notebook usage
DBFS file uploads, reads, writes
Cluster usage basics
Azure Databricks vs Community Edition
User management features (Azure only)