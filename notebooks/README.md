# Executer

## Table of Contents
- [Example Notebooks](#example-notebooks)
- [Setup Notebooks to Receive Parameters](#setup-notebooks-to-receive-parameters)

---

### Example Notebooks

![Jupyter Folder](/resource/iamges/notebooks/jupyter_folder.png "Jupyter Folder")

The image above shows a Jupyter folder containing multiple Jupyter notebooks.

---

### Setup Notebooks to Receive Parameters

![Jupyter Notebook](/resource/iamges/notebooks/jupyter_notebook.png "Jupyter Notebook")

The image above shows two main cells in a Jupyter notebook that are intended to be modified to support receiving parameters from Apache Airflow. While these cells are defined, the notebook is not yet capable of receiving parameters without additional setup.

---

![Navigate to JupyterLab](/resource/iamges/notebooks/navtojupyterlab.png "Nav to Jupyter Lab")

To enable notebooks to receive parameters, you need to extend the cell with parameter support. This can only be done in **JupyterLab**. Navigate to  
**View → Open in JupyterLab**.

---

![JupyterLab UI](/resource/iamges/notebooks/jupyterlab.png "Jupyter Lab")

Once inside JupyterLab, click the **"Common Tools"** icon in the upper-right corner.  
Then follow these steps:

1. Select the parameter cell.
2. Add the `parameters` tag to the cell under **Cell Tags**.
3. Set the slide type to `Skip`.
4. Save the changes.

After completing these steps, the notebook will be able to receive parameters passed from Apache Airflow. The notebooks will declare the parameters that have received parameter from Apache Airflow in the next cell as shown in the example below.

---

![Test Passing Parameter](/resource/iamges/notebooks/passingparameter.png "Test Passing Parameter")

The example above shows a successful parameter passing from Apache Airflow to a Jupyter notebook.

---
