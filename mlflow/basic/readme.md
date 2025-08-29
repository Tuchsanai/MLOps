Here’s a Markdown rendering of the MLflow documentation page you linked, **"Starting the MLflow Tracking Server"**:

---

````markdown
# Starting the MLflow Tracking Server

Before diving into MLflow's rich features, let's set up the foundational components: the MLflow Tracking Server and the MLflow UI. This guide will walk you through the steps to get both up and running.

## Setting Up MLflow

The first thing that we need to do is to get MLflow.

### Step 1: Install MLflow from PyPI

MLflow is conveniently available on PyPI. Installing it is as simple as running a pip command:

```bash
pip install mlflow
````

### Step 2 (Optional): Launch the MLflow Tracking Server

If you would like to use a simpler solution by leveraging a managed instance of the MLflow Tracking Server, please [see the details about options here](#) (reference to the original options page).

To begin, you'll need to initiate the MLflow Tracking Server. Remember to keep the command prompt running during the tutorial, as closing it will shut down the server.

```bash
mlflow server --host 127.0.0.1 --port 8080
```

Once the server starts running, you should see the following output:

```
INFO:     Started server process [28550]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

> **Note:**
> Remember the host and port name that your MLflow tracking server is assigned. You will need this information in the next section of this tutorial!

Congratulations! Your MLflow environment is now set up and ready to go. As you progress, you'll explore the myriad of functionalities MLflow has to offer, streamlining and enhancing your machine learning workflows.

You can now [continue to the next section (Using the MLflow Client API)](#) of the tutorial, or [return to the tutorial listing (#)](#).

```

---

### Notes on the Markdown rendering
- I've preserved the headings, code blocks, command outputs, and the inline note block.
- The internal links (e.g., to other sections or pages) are rendered as placeholders (`[#]`) since I can't resolve dynamic URLs directly—feel free to replace them with actual URLs if needed.
- Let me know if you'd like a Markdown version of the rest of the tutorial or other sections!
::contentReference[oaicite:0]{index=0}
```
