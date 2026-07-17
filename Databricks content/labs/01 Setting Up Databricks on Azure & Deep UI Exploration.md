LAB 2 — Setting Up Databricks on Azure & Deep UI Exploration


Estimated Time: 90 minutes

Objectives:

✔ Deploy Azure Databricks Workspace

✔ Explore all workspace components available only in Azure version

✔ Understand key concepts: Premium vs Standard tier

✔ Create cluster, notebook, repos, jobs

✔ Explore admin settings, access control, and workspace configuration



PART A — Create Azure Databricks Workspace

Step 1 — Log into Azure Portal
Open portal.azure.com.
Sign in using your Azure account.
Go to the Azure Home dashboard.
Ensure your subscription is active.
If not, activate Azure free trial.
Proceed to the next step.

Step 2 — Search for Azure Databricks
In Azure search bar, type “Databricks”.
Click Azure Databricks service.
Click Create.
You will land on the Workspace creation form.
Ensure you are in the correct subscription.
Select the correct Resource Group or create a new one.


Step 3 — Configure Workspace Settings
Choose workspace name: databricks-lab-ws01.
Select region closest to you.
Pricing tier: Premium (required for Unity Catalog).
Review Networking tab (keep defaults for now).
Disable custom VNet unless needed.
Click Review + Create → Create.

Step 4 — Launch Azure Databricks
Wait 4–8 minutes for deployment.
Click Go to Resource.
Click Launch Workspace.
A new Databricks workspace opens in a new tab.
You will now see the full Databricks UI (more features than CE).
Confirm left navigation shows Catalog (Unity Catalog) option.


PART B — Detailed UI Exploration (Azure Version)

Step 5 — Explore Catalog (Unity Catalog)
Click Catalog tab.
Explore catalogs → schemas → tables structure.
Observe system catalog like system and samples.
Notice permission levels and lineage options.
Compare this with Community Edition differences.
Do not modify any default catalog yet.

Step 6 — Explore Workspace Section
Click Workspace.
Open shared and user folders.
Review right-click menu options.
Check Import/Export features.
Explore folder permissions.
Look at Repos integration in this view.

Step 7 — Explore Repos
Click Repos on left nav.
Click Add Repo.
Connect with GitHub or Azure DevOps.
Select OAuth → Authenticate.
Clone a test repo (optional).
Observe version control capabilities.

Step 8 — Explore Data Section
Click Data.
Explore catalog/schemas.
Check permissions tab.
Navigate to lineage to see relationships.
Open sample tables like diamonds.
Preview data via View Details.


Step 9 — Explore Compute Section
Go to Compute.
Click Create Cluster.
Name cluster: azure-lab-cluster.
Runtime: choose latest 12.x or above.
Worker type: Standard_DS3_v2.
Click Create.

Step 10 — Explore Cluster Features
Click cluster name.
Explore Configuration tab.
Explore Libraries tab.
Explore Spark UI tab.
Explore Metrics tab.
Explore Event Log tab.


PART C — Build First Notebook in Azure Databricks

Step 11 — Create Notebook
Go to Workspace.
Click Create → Notebook.
Name: Azure_Databricks_Intro.
Choose Python as language.
Attach to the Azure cluster.

Step 12 — Execute First Commands
Run spark.range(10).show().
Run dbutils.fs.ls("/").
Add markdown cell documenting your actions.
Add visualization cell using display().
Save the notebook.

Lab 2 Completion Criteria


✔ You deployed Azure Databricks Workspace

✔ You explored Unity Catalog, Repos, Data, SQL, Compute

✔ You created and ran a notebook

✔ You created a cluster and explored detailed tabs

✔ You compared CE vs Azure capabilities