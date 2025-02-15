{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Project1.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "toc_visible": true,
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/SerenaD005/CS634-DataMiningProject-1/blob/master/Midterm.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JRYgpzp-3ZPB",
        "colab_type": "text"
      },
      "source": [
        "# **PROJECT**: **[Google Analytics Customer Revenue Prediction](https://www.kaggle.com/c/ga-customer-revenue-prediction/overview)**"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "u-X9WkG3QKR4",
        "colab_type": "text"
      },
      "source": [
        "#### **The fundamental steps we will be taking in this project are:**\n",
        "\n",
        "\n",
        ">1.   **Understand the Objective of this project**\n",
        "2.   **Data Collection & Data Preperation**\n",
        "3.   **Modeling & Evaluation**\n",
        "4.   **Communicate/Present Results**\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "_OcdqZyqKEhs",
        "colab_type": "text"
      },
      "source": [
        "# **1 - Understanding the Objective**\n",
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "9wU-yXsnHATp",
        "colab_type": "text"
      },
      "source": [
        "### **Predict how much GStore customers will spend**\n",
        "\n",
        "In this [Project](https://www.kaggle.com/c/ga-customer-revenue-prediction/overview), we’re challenged to analyze a Google Merchandise Store (also known as GStore, where Google swag is sold) customer dataset to **predict revenue per customer**.\n",
        " \n",
        "**What are we predicting?**\n",
        "\n",
        "We are predicting the natural log of the sum of all transactions per user.\n",
        "\n",
        "**Evaluation Metric**\n",
        "\n",
        "***`RMSE`*** - *Root Mean Squared Error*\n",
        "\n",
        "**RMSE** is the standard deviation of residuals (predictions errors). When we scatter plot the target_test values and predictions, the RMSE tells us how concentrated are those points around the line of best fit.\n",
        "\n",
        "![RSME](./rsme.jpg)\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "ghmLuPovKfkx"
      },
      "source": [
        "# **2 - Data Collection & Data Preperation**\n",
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JMBjve1qu2-G",
        "colab_type": "text"
      },
      "source": [
        "## **Mount** the **Google** **Drive** on to the Notebook.\n",
        "\n",
        "\n",
        "---"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "U2q-kEm-utZA",
        "colab_type": "code",
        "outputId": "74f5dee2-ffcb-47ad-b012-ba5a18eaa3ab",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 74
        }
      },
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount(\"/content/drive\", force_remount=True).\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "X0zyLM2SCF0B",
        "colab_type": "code",
        "outputId": "ed1fa837-46e2-4e77-b640-765ca99d1c54",
        "colab": {
          "resources": {
            "http://localhost:8080/nbextensions/google.colab/files.js": {
              "data": "Ly8gQ29weXJpZ2h0IDIwMTcgR29vZ2xlIExMQwovLwovLyBMaWNlbnNlZCB1bmRlciB0aGUgQXBhY2hlIExpY2Vuc2UsIFZlcnNpb24gMi4wICh0aGUgIkxpY2Vuc2UiKTsKLy8geW91IG1heSBub3QgdXNlIHRoaXMgZmlsZSBleGNlcHQgaW4gY29tcGxpYW5jZSB3aXRoIHRoZSBMaWNlbnNlLgovLyBZb3UgbWF5IG9idGFpbiBhIGNvcHkgb2YgdGhlIExpY2Vuc2UgYXQKLy8KLy8gICAgICBodHRwOi8vd3d3LmFwYWNoZS5vcmcvbGljZW5zZXMvTElDRU5TRS0yLjAKLy8KLy8gVW5sZXNzIHJlcXVpcmVkIGJ5IGFwcGxpY2FibGUgbGF3IG9yIGFncmVlZCB0byBpbiB3cml0aW5nLCBzb2Z0d2FyZQovLyBkaXN0cmlidXRlZCB1bmRlciB0aGUgTGljZW5zZSBpcyBkaXN0cmlidXRlZCBvbiBhbiAiQVMgSVMiIEJBU0lTLAovLyBXSVRIT1VUIFdBUlJBTlRJRVMgT1IgQ09ORElUSU9OUyBPRiBBTlkgS0lORCwgZWl0aGVyIGV4cHJlc3Mgb3IgaW1wbGllZC4KLy8gU2VlIHRoZSBMaWNlbnNlIGZvciB0aGUgc3BlY2lmaWMgbGFuZ3VhZ2UgZ292ZXJuaW5nIHBlcm1pc3Npb25zIGFuZAovLyBsaW1pdGF0aW9ucyB1bmRlciB0aGUgTGljZW5zZS4KCi8qKgogKiBAZmlsZW92ZXJ2aWV3IEhlbHBlcnMgZm9yIGdvb2dsZS5jb2xhYiBQeXRob24gbW9kdWxlLgogKi8KKGZ1bmN0aW9uKHNjb3BlKSB7CmZ1bmN0aW9uIHNwYW4odGV4dCwgc3R5bGVBdHRyaWJ1dGVzID0ge30pIHsKICBjb25zdCBlbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3BhbicpOwogIGVsZW1lbnQudGV4dENvbnRlbnQgPSB0ZXh0OwogIGZvciAoY29uc3Qga2V5IG9mIE9iamVjdC5rZXlzKHN0eWxlQXR0cmlidXRlcykpIHsKICAgIGVsZW1lbnQuc3R5bGVba2V5XSA9IHN0eWxlQXR0cmlidXRlc1trZXldOwogIH0KICByZXR1cm4gZWxlbWVudDsKfQoKLy8gTWF4IG51bWJlciBvZiBieXRlcyB3aGljaCB3aWxsIGJlIHVwbG9hZGVkIGF0IGEgdGltZS4KY29uc3QgTUFYX1BBWUxPQURfU0laRSA9IDEwMCAqIDEwMjQ7Ci8vIE1heCBhbW91bnQgb2YgdGltZSB0byBibG9jayB3YWl0aW5nIGZvciB0aGUgdXNlci4KY29uc3QgRklMRV9DSEFOR0VfVElNRU9VVF9NUyA9IDMwICogMTAwMDsKCmZ1bmN0aW9uIF91cGxvYWRGaWxlcyhpbnB1dElkLCBvdXRwdXRJZCkgewogIGNvbnN0IHN0ZXBzID0gdXBsb2FkRmlsZXNTdGVwKGlucHV0SWQsIG91dHB1dElkKTsKICBjb25zdCBvdXRwdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQob3V0cHV0SWQpOwogIC8vIENhY2hlIHN0ZXBzIG9uIHRoZSBvdXRwdXRFbGVtZW50IHRvIG1ha2UgaXQgYXZhaWxhYmxlIGZvciB0aGUgbmV4dCBjYWxsCiAgLy8gdG8gdXBsb2FkRmlsZXNDb250aW51ZSBmcm9tIFB5dGhvbi4KICBvdXRwdXRFbGVtZW50LnN0ZXBzID0gc3RlcHM7CgogIHJldHVybiBfdXBsb2FkRmlsZXNDb250aW51ZShvdXRwdXRJZCk7Cn0KCi8vIFRoaXMgaXMgcm91Z2hseSBhbiBhc3luYyBnZW5lcmF0b3IgKG5vdCBzdXBwb3J0ZWQgaW4gdGhlIGJyb3dzZXIgeWV0KSwKLy8gd2hlcmUgdGhlcmUgYXJlIG11bHRpcGxlIGFzeW5jaHJvbm91cyBzdGVwcyBhbmQgdGhlIFB5dGhvbiBzaWRlIGlzIGdvaW5nCi8vIHRvIHBvbGwgZm9yIGNvbXBsZXRpb24gb2YgZWFjaCBzdGVwLgovLyBUaGlzIHVzZXMgYSBQcm9taXNlIHRvIGJsb2NrIHRoZSBweXRob24gc2lkZSBvbiBjb21wbGV0aW9uIG9mIGVhY2ggc3RlcCwKLy8gdGhlbiBwYXNzZXMgdGhlIHJlc3VsdCBvZiB0aGUgcHJldmlvdXMgc3RlcCBhcyB0aGUgaW5wdXQgdG8gdGhlIG5leHQgc3RlcC4KZnVuY3Rpb24gX3VwbG9hZEZpbGVzQ29udGludWUob3V0cHV0SWQpIHsKICBjb25zdCBvdXRwdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQob3V0cHV0SWQpOwogIGNvbnN0IHN0ZXBzID0gb3V0cHV0RWxlbWVudC5zdGVwczsKCiAgY29uc3QgbmV4dCA9IHN0ZXBzLm5leHQob3V0cHV0RWxlbWVudC5sYXN0UHJvbWlzZVZhbHVlKTsKICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKG5leHQudmFsdWUucHJvbWlzZSkudGhlbigodmFsdWUpID0+IHsKICAgIC8vIENhY2hlIHRoZSBsYXN0IHByb21pc2UgdmFsdWUgdG8gbWFrZSBpdCBhdmFpbGFibGUgdG8gdGhlIG5leHQKICAgIC8vIHN0ZXAgb2YgdGhlIGdlbmVyYXRvci4KICAgIG91dHB1dEVsZW1lbnQubGFzdFByb21pc2VWYWx1ZSA9IHZhbHVlOwogICAgcmV0dXJuIG5leHQudmFsdWUucmVzcG9uc2U7CiAgfSk7Cn0KCi8qKgogKiBHZW5lcmF0b3IgZnVuY3Rpb24gd2hpY2ggaXMgY2FsbGVkIGJldHdlZW4gZWFjaCBhc3luYyBzdGVwIG9mIHRoZSB1cGxvYWQKICogcHJvY2Vzcy4KICogQHBhcmFtIHtzdHJpbmd9IGlucHV0SWQgRWxlbWVudCBJRCBvZiB0aGUgaW5wdXQgZmlsZSBwaWNrZXIgZWxlbWVudC4KICogQHBhcmFtIHtzdHJpbmd9IG91dHB1dElkIEVsZW1lbnQgSUQgb2YgdGhlIG91dHB1dCBkaXNwbGF5LgogKiBAcmV0dXJuIHshSXRlcmFibGU8IU9iamVjdD59IEl0ZXJhYmxlIG9mIG5leHQgc3RlcHMuCiAqLwpmdW5jdGlvbiogdXBsb2FkRmlsZXNTdGVwKGlucHV0SWQsIG91dHB1dElkKSB7CiAgY29uc3QgaW5wdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoaW5wdXRJZCk7CiAgaW5wdXRFbGVtZW50LmRpc2FibGVkID0gZmFsc2U7CgogIGNvbnN0IG91dHB1dEVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChvdXRwdXRJZCk7CiAgb3V0cHV0RWxlbWVudC5pbm5lckhUTUwgPSAnJzsKCiAgY29uc3QgcGlja2VkUHJvbWlzZSA9IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7CiAgICBpbnB1dEVsZW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignY2hhbmdlJywgKGUpID0+IHsKICAgICAgcmVzb2x2ZShlLnRhcmdldC5maWxlcyk7CiAgICB9KTsKICB9KTsKCiAgY29uc3QgY2FuY2VsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYnV0dG9uJyk7CiAgaW5wdXRFbGVtZW50LnBhcmVudEVsZW1lbnQuYXBwZW5kQ2hpbGQoY2FuY2VsKTsKICBjYW5jZWwudGV4dENvbnRlbnQgPSAnQ2FuY2VsIHVwbG9hZCc7CiAgY29uc3QgY2FuY2VsUHJvbWlzZSA9IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7CiAgICBjYW5jZWwub25jbGljayA9ICgpID0+IHsKICAgICAgcmVzb2x2ZShudWxsKTsKICAgIH07CiAgfSk7CgogIC8vIENhbmNlbCB1cGxvYWQgaWYgdXNlciBoYXNuJ3QgcGlja2VkIGFueXRoaW5nIGluIHRpbWVvdXQuCiAgY29uc3QgdGltZW91dFByb21pc2UgPSBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gewogICAgc2V0VGltZW91dCgoKSA9PiB7CiAgICAgIHJlc29sdmUobnVsbCk7CiAgICB9LCBGSUxFX0NIQU5HRV9USU1FT1VUX01TKTsKICB9KTsKCiAgLy8gV2FpdCBmb3IgdGhlIHVzZXIgdG8gcGljayB0aGUgZmlsZXMuCiAgY29uc3QgZmlsZXMgPSB5aWVsZCB7CiAgICBwcm9taXNlOiBQcm9taXNlLnJhY2UoW3BpY2tlZFByb21pc2UsIHRpbWVvdXRQcm9taXNlLCBjYW5jZWxQcm9taXNlXSksCiAgICByZXNwb25zZTogewogICAgICBhY3Rpb246ICdzdGFydGluZycsCiAgICB9CiAgfTsKCiAgaWYgKCFmaWxlcykgewogICAgcmV0dXJuIHsKICAgICAgcmVzcG9uc2U6IHsKICAgICAgICBhY3Rpb246ICdjb21wbGV0ZScsCiAgICAgIH0KICAgIH07CiAgfQoKICBjYW5jZWwucmVtb3ZlKCk7CgogIC8vIERpc2FibGUgdGhlIGlucHV0IGVsZW1lbnQgc2luY2UgZnVydGhlciBwaWNrcyBhcmUgbm90IGFsbG93ZWQuCiAgaW5wdXRFbGVtZW50LmRpc2FibGVkID0gdHJ1ZTsKCiAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7CiAgICBjb25zdCBsaSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2xpJyk7CiAgICBsaS5hcHBlbmQoc3BhbihmaWxlLm5hbWUsIHtmb250V2VpZ2h0OiAnYm9sZCd9KSk7CiAgICBsaS5hcHBlbmQoc3BhbigKICAgICAgICBgKCR7ZmlsZS50eXBlIHx8ICduL2EnfSkgLSAke2ZpbGUuc2l6ZX0gYnl0ZXMsIGAgKwogICAgICAgIGBsYXN0IG1vZGlmaWVkOiAkewogICAgICAgICAgICBmaWxlLmxhc3RNb2RpZmllZERhdGUgPyBmaWxlLmxhc3RNb2RpZmllZERhdGUudG9Mb2NhbGVEYXRlU3RyaW5nKCkgOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnbi9hJ30gLSBgKSk7CiAgICBjb25zdCBwZXJjZW50ID0gc3BhbignMCUgZG9uZScpOwogICAgbGkuYXBwZW5kQ2hpbGQocGVyY2VudCk7CgogICAgb3V0cHV0RWxlbWVudC5hcHBlbmRDaGlsZChsaSk7CgogICAgY29uc3QgZmlsZURhdGFQcm9taXNlID0gbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHsKICAgICAgY29uc3QgcmVhZGVyID0gbmV3IEZpbGVSZWFkZXIoKTsKICAgICAgcmVhZGVyLm9ubG9hZCA9IChlKSA9PiB7CiAgICAgICAgcmVzb2x2ZShlLnRhcmdldC5yZXN1bHQpOwogICAgICB9OwogICAgICByZWFkZXIucmVhZEFzQXJyYXlCdWZmZXIoZmlsZSk7CiAgICB9KTsKICAgIC8vIFdhaXQgZm9yIHRoZSBkYXRhIHRvIGJlIHJlYWR5LgogICAgbGV0IGZpbGVEYXRhID0geWllbGQgewogICAgICBwcm9taXNlOiBmaWxlRGF0YVByb21pc2UsCiAgICAgIHJlc3BvbnNlOiB7CiAgICAgICAgYWN0aW9uOiAnY29udGludWUnLAogICAgICB9CiAgICB9OwoKICAgIC8vIFVzZSBhIGNodW5rZWQgc2VuZGluZyB0byBhdm9pZCBtZXNzYWdlIHNpemUgbGltaXRzLiBTZWUgYi82MjExNTY2MC4KICAgIGxldCBwb3NpdGlvbiA9IDA7CiAgICB3aGlsZSAocG9zaXRpb24gPCBmaWxlRGF0YS5ieXRlTGVuZ3RoKSB7CiAgICAgIGNvbnN0IGxlbmd0aCA9IE1hdGgubWluKGZpbGVEYXRhLmJ5dGVMZW5ndGggLSBwb3NpdGlvbiwgTUFYX1BBWUxPQURfU0laRSk7CiAgICAgIGNvbnN0IGNodW5rID0gbmV3IFVpbnQ4QXJyYXkoZmlsZURhdGEsIHBvc2l0aW9uLCBsZW5ndGgpOwogICAgICBwb3NpdGlvbiArPSBsZW5ndGg7CgogICAgICBjb25zdCBiYXNlNjQgPSBidG9hKFN0cmluZy5mcm9tQ2hhckNvZGUuYXBwbHkobnVsbCwgY2h1bmspKTsKICAgICAgeWllbGQgewogICAgICAgIHJlc3BvbnNlOiB7CiAgICAgICAgICBhY3Rpb246ICdhcHBlbmQnLAogICAgICAgICAgZmlsZTogZmlsZS5uYW1lLAogICAgICAgICAgZGF0YTogYmFzZTY0LAogICAgICAgIH0sCiAgICAgIH07CiAgICAgIHBlcmNlbnQudGV4dENvbnRlbnQgPQogICAgICAgICAgYCR7TWF0aC5yb3VuZCgocG9zaXRpb24gLyBmaWxlRGF0YS5ieXRlTGVuZ3RoKSAqIDEwMCl9JSBkb25lYDsKICAgIH0KICB9CgogIC8vIEFsbCBkb25lLgogIHlpZWxkIHsKICAgIHJlc3BvbnNlOiB7CiAgICAgIGFjdGlvbjogJ2NvbXBsZXRlJywKICAgIH0KICB9Owp9CgpzY29wZS5nb29nbGUgPSBzY29wZS5nb29nbGUgfHwge307CnNjb3BlLmdvb2dsZS5jb2xhYiA9IHNjb3BlLmdvb2dsZS5jb2xhYiB8fCB7fTsKc2NvcGUuZ29vZ2xlLmNvbGFiLl9maWxlcyA9IHsKICBfdXBsb2FkRmlsZXMsCiAgX3VwbG9hZEZpbGVzQ29udGludWUsCn07Cn0pKHNlbGYpOwo=",
              "ok": true,
              "headers": [
                [
                  "content-type",
                  "application/javascript"
                ]
              ],
              "status": 200,
              "status_text": ""
            }
          },
          "base_uri": "https://localhost:8080/",
          "height": 75
        }
      },
      "source": [
        "# to load kaggle API\n",
        "!pip install -q kaggle \n",
        "from google.colab import files \n",
        "uploaded = files.upload()"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "\n",
              "     <input type=\"file\" id=\"files-f222d62b-3c4e-4dd9-a451-f493d7cc1698\" name=\"files[]\" multiple disabled />\n",
              "     <output id=\"result-f222d62b-3c4e-4dd9-a451-f493d7cc1698\">\n",
              "      Upload widget is only available when the cell has been executed in the\n",
              "      current browser session. Please rerun this cell to enable.\n",
              "      </output>\n",
              "      <script src=\"/nbextensions/google.colab/files.js\"></script> "
            ],
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "Saving kaggle.json to kaggle (1).json\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qi6fFIT_CQf0",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "!mkdir -p ~/.kaggle\n",
        "!cp kaggle.json ~/.kaggle/"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "gU7ORYOEClCw",
        "colab_type": "code",
        "outputId": "252bd669-4e57-4612-a15d-ec8077440155",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 102
        }
      },
      "source": [
        "#now we install 7zip\n",
        "!apt-get install p7zip-full"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Reading package lists... Done\n",
            "Building dependency tree       \n",
            "Reading state information... Done\n",
            "p7zip-full is already the newest version (16.02+dfsg-6).\n",
            "0 upgraded, 0 newly installed, 0 to remove and 35 not upgraded.\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "KLjiKwc6Cq1L",
        "colab_type": "code",
        "outputId": "09bc9e54-f0dd-418f-bf86-e877d7894026",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 123
        }
      },
      "source": [
        "!kaggle datasets download -d niteshmistry/minigacustomerrevenueprediction"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Warning: Your Kaggle API key is readable by other users on this system! To fix this, you can run 'chmod 600 /root/.kaggle/kaggle.json'\n",
            "minigacustomerrevenueprediction.zip: Skipping, found more recently modified local copy (use --force to force download)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "yeygSTiTCw3Z",
        "colab_type": "code",
        "outputId": "d37a1fe8-77f7-4492-e7b9-66d675f827bf",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 801
        }
      },
      "source": [
        "!7za e minigacustomerrevenueprediction.zip"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "\n",
            "7-Zip (a) [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21\n",
            "p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,2 CPUs Intel(R) Xeon(R) CPU @ 2.30GHz (306F0),ASM,AES-NI)\n",
            "\n",
            "Scanning the drive for archives:\n",
            "  0M Scan\b\b\b\b\b\b\b\b\b         \b\b\b\b\b\b\b\b\b1 file, 16767918 bytes (16 MiB)\n",
            "\n",
            "Extracting archive: minigacustomerrevenueprediction.zip\n",
            "--\n",
            "Path = minigacustomerrevenueprediction.zip\n",
            "Type = zip\n",
            "Physical Size = 16767918\n",
            "\n",
            "  0%\b\b\b\b    \b\b\b\b\n",
            "Would you like to replace the existing file:\n",
            "  Path:     ./mini-test.csv\n",
            "  Size:     33552335 bytes (32 MiB)\n",
            "  Modified: 2019-11-02 19:51:56\n",
            "with the file from archive:\n",
            "  Path:     mini-test.csv\n",
            "  Size:     33552335 bytes (32 MiB)\n",
            "  Modified: 2019-11-02 19:51:56\n",
            "? (Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? y\n",
            "\n",
            "  0% - mini-test.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                    \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\n",
            "Would you like to replace the existing file:\n",
            "  Path:     ./mini-train.csv\n",
            "  Size:     325178219 bytes (311 MiB)\n",
            "  Modified: 2019-11-02 19:52:00\n",
            "with the file from archive:\n",
            "  Path:     mini-train.csv\n",
            "  Size:     325178219 bytes (311 MiB)\n",
            "  Modified: 2019-11-02 19:52:00\n",
            "? (Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? y\n",
            "\n",
            "  9% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 22% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 34% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 43% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 54% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 65% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 78% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b 91% 1 - mini-train.csv\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b                       \b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bEverything is Ok\n",
            "\n",
            "Files: 2\n",
            "Size:       358730554\n",
            "Compressed: 16767918\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "Ni7QQp6xwjfR"
      },
      "source": [
        "## **Import** the necessary **libraries** that are required to run this notebook:\n",
        "---\n",
        ">1. **JSON**\n",
        "2. **Pandas**\n",
        "3. **NumPy**\n",
        "4. **MatPlotLib**\n",
        "5. **Plotly**  - Plot graphs\n",
        "6. **SKLearn** - For model selection, preprocessing, metrics\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab_type": "code",
        "id": "WAxWFR3014rL",
        "colab": {}
      },
      "source": [
        "import os\n",
        "import time\n",
        "import json\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "from pandas.io.json import json_normalize\n",
        "import matplotlib.pyplot as plt\n",
        "from matplotlib.ticker import StrMethodFormatter\n",
        "from sklearn import linear_model\n",
        "from sklearn.model_selection import train_test_split\n",
        "\n",
        "%matplotlib inline\n"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "itYfivY-13aH"
      },
      "source": [
        "## **Datasets** that are required for this project that are necessary to run the notebook :\n",
        "---\n",
        ">1. **TRAIN Dataset** - *`train.csv`* (315 MB)\n",
        "2. **TEST Dataset** - *`test.csv`* (32 MB)\n",
        "\n",
        "### Each row in the dataset is one visit to the store. We are predicting the natural log of the sum of all transactions per user.\n",
        "\n",
        "## The **data fields** in the given files are\n",
        "\n",
        "* **fullVisitorId**- A unique identifier for each user of the Google Merchandise Store.\n",
        "* **channelGrouping** - The channel via which the user came to the Store.\n",
        "* **date** - The date on which the user visited the Store.\n",
        "* **device** - The specifications for the device used to access the Store.\n",
        "* **geoNetwork** - This section contains information about the geography of the user.\n",
        "* **sessionId** - A unique identifier for this visit to the store.\n",
        "* **socialEngagementType** - Engagement type, either \"Socially Engaged\" or \"Not Socially Engaged\".\n",
        "* **totals** - This section contains aggregate values across the session.\n",
        "* **trafficSource** - This section contains information about the Traffic Source from which the session originated.\n",
        "* **visitId** - An identifier for this session. This is part of the value usually stored as the _utmb cookie. This is only unique to the user. For a completely unique ID, you should use a combination of fullVisitorId and visitId.\n",
        "* **visitNumber** - The session number for this user. If this is the first session, then this is set to 1.\n",
        "* **visitStartTime** - The timestamp (expressed as POSIX time).\n",
        "\n",
        "***NOTE***: Some of the fields are in json format. We will have to transform them into Dataframe\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ux5ZG4TwWCxl",
        "colab_type": "text"
      },
      "source": [
        "## **LOAD** the data files that are required:\n",
        "---"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NKFpK2CFWh9Y",
        "colab_type": "code",
        "outputId": "a4575614-c86f-4334-dfb8-a222935633c9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 544
        }
      },
      "source": [
        "TRAIN_FILE = '/content/mini-train.csv'\n",
        "TEST_FILE = '/content/mini-test.csv'\n",
        "\n",
        "#------------------------------------------------------------------------------------------------\n",
        "# COMMON CSV DATA FILE LOADER - RETURN DATAFRAME\n",
        "#------------------------------------------------------------------------------------------------\n",
        "\n",
        "def convertCSVtoDF(csv_path, nrows):\n",
        "\n",
        "    df = pd.read_csv(csv_path, dtype={\"fullVisitorId\": \"str\"}, nrows=nrows)\n",
        "    print(f\"LOADED: {os.path.basename(csv_path)}   SHAPE: {df.shape}\")\n",
        "    \n",
        "    return df\n",
        "\n",
        "#------------------------------------------------------------------------------------------------\n",
        "# LOAD TRAINING DATASET file into DATAFRAME\n",
        "#------------------------------------------------------------------------------------------------\n",
        "train_df = convertCSVtoDF(TRAIN_FILE,None)\n",
        "test_df = convertCSVtoDF(TEST_FILE,None)\n",
        "\n",
        "#------------------------------------------------------------------------------------------------\n",
        "# LISTING HEADERS AND SAMPLE RECORDS (5)\n",
        "#------------------------------------------------------------------------------------------------\n",
        "print(\"\\n\")\n",
        "print(train_df.columns)\n"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "LOADED: mini-train.csv   SHAPE: (20000, 59)\n",
            "LOADED: mini-test.csv   SHAPE: (2000, 59)\n",
            "\n",
            "\n",
            "Index(['channelGrouping', 'customDimensions', 'date', 'fullVisitorId', 'hits',\n",
            "       'socialEngagementType', 'visitId', 'visitNumber', 'visitStartTime',\n",
            "       'device.browser', 'device.browserSize', 'device.browserVersion',\n",
            "       'device.deviceCategory', 'device.flashVersion', 'device.isMobile',\n",
            "       'device.language', 'device.mobileDeviceBranding',\n",
            "       'device.mobileDeviceInfo', 'device.mobileDeviceMarketingName',\n",
            "       'device.mobileDeviceModel', 'device.mobileInputSelector',\n",
            "       'device.operatingSystem', 'device.operatingSystemVersion',\n",
            "       'device.screenColors', 'device.screenResolution', 'geoNetwork.city',\n",
            "       'geoNetwork.cityId', 'geoNetwork.continent', 'geoNetwork.country',\n",
            "       'geoNetwork.latitude', 'geoNetwork.longitude', 'geoNetwork.metro',\n",
            "       'geoNetwork.networkDomain', 'geoNetwork.networkLocation',\n",
            "       'geoNetwork.region', 'geoNetwork.subContinent', 'totals.bounces',\n",
            "       'totals.hits', 'totals.newVisits', 'totals.pageviews',\n",
            "       'totals.sessionQualityDim', 'totals.timeOnSite',\n",
            "       'totals.totalTransactionRevenue', 'totals.transactionRevenue',\n",
            "       'totals.transactions', 'totals.visits', 'trafficSource.adContent',\n",
            "       'trafficSource.adwordsClickInfo.adNetworkType',\n",
            "       'trafficSource.adwordsClickInfo.criteriaParameters',\n",
            "       'trafficSource.adwordsClickInfo.gclId',\n",
            "       'trafficSource.adwordsClickInfo.isVideoAd',\n",
            "       'trafficSource.adwordsClickInfo.page',\n",
            "       'trafficSource.adwordsClickInfo.slot', 'trafficSource.campaign',\n",
            "       'trafficSource.isTrueDirect', 'trafficSource.keyword',\n",
            "       'trafficSource.medium', 'trafficSource.referralPath',\n",
            "       'trafficSource.source'],\n",
            "      dtype='object')\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-pS5ABNd5jcn",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "#------------------------------------------------------------------------------------------------\n",
        "# FUNCTION REMOVING EMPTY COLUMNS with value \"not available in demo dataset\"\n",
        "#------------------------------------------------------------------------------------------------\n",
        "\n",
        "def removeUselessColumns(df):\n",
        "  EMPTY_COLUMNS = []\n",
        "\n",
        "  dataframe = df\n",
        "\n",
        "  for column in train_df.columns:\n",
        "    if train_df[column][0] == 'not available in demo dataset':\n",
        "      EMPTY_COLUMNS.append(column)\n",
        "  \n",
        "  print(\"DATAFRAME IS \" + str(len(dataframe.columns)) + \" COLUMNS...\")\n",
        "  print(\"FOUND \" + str(len(EMPTY_COLUMNS)) + \" USELESS COLUMNS...\")\n",
        "  print(\"COLUMNS:  \" + str(EMPTY_COLUMNS))\n",
        "  print(\"REMOVING \" + str(len(EMPTY_COLUMNS)) + \" COLUMNS...\")\n",
        "  dataframe.drop(EMPTY_COLUMNS, axis=1, inplace=True)\n",
        "  print(\"DATAFRAME IS NOW \" + str(len(dataframe.columns)) + \" COLUMNS...\")\n",
        "\n",
        "  return dataframe\n",
        "\n"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ijT7k9-W5wqP",
        "colab_type": "text"
      },
      "source": [
        "\n",
        "**REMOVE USELESS COLUMNS** that has values \"**NOT AVAILABLE IN DEMO DATASET**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "wHQDZ6xgF52G",
        "colab_type": "code",
        "outputId": "9b4bff65-9e94-426f-f00a-fc26f46e2f7d",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 499
        }
      },
      "source": [
        "#------------------------------------------------------------------------------------------------\n",
        "# TRAINING DATAFRAME - REMOVING EMPTY COLUMNS with value \"not available in demo dataset\"\n",
        "#------------------------------------------------------------------------------------------------\n",
        "\n",
        "train_df = removeUselessColumns(train_df)\n",
        "train_df.head(5)"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "DATAFRAME IS 59 COLUMNS...\n",
            "FOUND 20 USELESS COLUMNS...\n",
            "COLUMNS:  ['device.browserSize', 'device.browserVersion', 'device.flashVersion', 'device.language', 'device.mobileDeviceBranding', 'device.mobileDeviceInfo', 'device.mobileDeviceMarketingName', 'device.mobileDeviceModel', 'device.mobileInputSelector', 'device.operatingSystemVersion', 'device.screenColors', 'device.screenResolution', 'geoNetwork.city', 'geoNetwork.cityId', 'geoNetwork.latitude', 'geoNetwork.longitude', 'geoNetwork.metro', 'geoNetwork.networkLocation', 'geoNetwork.region', 'trafficSource.adwordsClickInfo.criteriaParameters']\n",
            "REMOVING 20 COLUMNS...\n",
            "DATAFRAME IS NOW 39 COLUMNS...\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>channelGrouping</th>\n",
              "      <th>customDimensions</th>\n",
              "      <th>date</th>\n",
              "      <th>fullVisitorId</th>\n",
              "      <th>hits</th>\n",
              "      <th>socialEngagementType</th>\n",
              "      <th>visitId</th>\n",
              "      <th>visitNumber</th>\n",
              "      <th>visitStartTime</th>\n",
              "      <th>device.browser</th>\n",
              "      <th>device.deviceCategory</th>\n",
              "      <th>device.isMobile</th>\n",
              "      <th>device.operatingSystem</th>\n",
              "      <th>geoNetwork.continent</th>\n",
              "      <th>geoNetwork.country</th>\n",
              "      <th>geoNetwork.networkDomain</th>\n",
              "      <th>geoNetwork.subContinent</th>\n",
              "      <th>totals.bounces</th>\n",
              "      <th>totals.hits</th>\n",
              "      <th>totals.newVisits</th>\n",
              "      <th>totals.pageviews</th>\n",
              "      <th>totals.sessionQualityDim</th>\n",
              "      <th>totals.timeOnSite</th>\n",
              "      <th>totals.totalTransactionRevenue</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "      <th>totals.transactions</th>\n",
              "      <th>totals.visits</th>\n",
              "      <th>trafficSource.adContent</th>\n",
              "      <th>trafficSource.adwordsClickInfo.adNetworkType</th>\n",
              "      <th>trafficSource.adwordsClickInfo.gclId</th>\n",
              "      <th>trafficSource.adwordsClickInfo.isVideoAd</th>\n",
              "      <th>trafficSource.adwordsClickInfo.page</th>\n",
              "      <th>trafficSource.adwordsClickInfo.slot</th>\n",
              "      <th>trafficSource.campaign</th>\n",
              "      <th>trafficSource.isTrueDirect</th>\n",
              "      <th>trafficSource.keyword</th>\n",
              "      <th>trafficSource.medium</th>\n",
              "      <th>trafficSource.referralPath</th>\n",
              "      <th>trafficSource.source</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'EMEA'}]</td>\n",
              "      <td>20171016</td>\n",
              "      <td>3162355547410993243</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '17',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1508198450</td>\n",
              "      <td>1</td>\n",
              "      <td>1508198450</td>\n",
              "      <td>Firefox</td>\n",
              "      <td>desktop</td>\n",
              "      <td>False</td>\n",
              "      <td>Windows</td>\n",
              "      <td>Europe</td>\n",
              "      <td>Germany</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>Western Europe</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>water bottle</td>\n",
              "      <td>organic</td>\n",
              "      <td>NaN</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Referral</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20171016</td>\n",
              "      <td>8934116514970143966</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '10',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1508176307</td>\n",
              "      <td>6</td>\n",
              "      <td>1508176307</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>desktop</td>\n",
              "      <td>False</td>\n",
              "      <td>Chrome OS</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>2</td>\n",
              "      <td>NaN</td>\n",
              "      <td>2.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>28.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>referral</td>\n",
              "      <td>/a/google.com/transportation/mtv-services/bike...</td>\n",
              "      <td>sites.google.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Direct</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20171016</td>\n",
              "      <td>7992466427990357681</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '17',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1508201613</td>\n",
              "      <td>1</td>\n",
              "      <td>1508201613</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>mobile</td>\n",
              "      <td>True</td>\n",
              "      <td>Android</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>windjammercable.net</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>2</td>\n",
              "      <td>1.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>38.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>True</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(none)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(direct)</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'EMEA'}]</td>\n",
              "      <td>20171016</td>\n",
              "      <td>9075655783635761930</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '9', ...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1508169851</td>\n",
              "      <td>1</td>\n",
              "      <td>1508169851</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>desktop</td>\n",
              "      <td>False</td>\n",
              "      <td>Windows</td>\n",
              "      <td>Asia</td>\n",
              "      <td>Turkey</td>\n",
              "      <td>unknown.unknown</td>\n",
              "      <td>Western Asia</td>\n",
              "      <td>NaN</td>\n",
              "      <td>2</td>\n",
              "      <td>1.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not provided)</td>\n",
              "      <td>organic</td>\n",
              "      <td>NaN</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'Central America'}]</td>\n",
              "      <td>20171016</td>\n",
              "      <td>6960673291025684308</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '14',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1508190552</td>\n",
              "      <td>1</td>\n",
              "      <td>1508190552</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>desktop</td>\n",
              "      <td>False</td>\n",
              "      <td>Windows</td>\n",
              "      <td>Americas</td>\n",
              "      <td>Mexico</td>\n",
              "      <td>prod-infinitum.com.mx</td>\n",
              "      <td>Central America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>2</td>\n",
              "      <td>1.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>52.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not provided)</td>\n",
              "      <td>organic</td>\n",
              "      <td>NaN</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "  channelGrouping  ... trafficSource.source\n",
              "0  Organic Search  ...               google\n",
              "1        Referral  ...     sites.google.com\n",
              "2          Direct  ...             (direct)\n",
              "3  Organic Search  ...               google\n",
              "4  Organic Search  ...               google\n",
              "\n",
              "[5 rows x 39 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 60
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "RrUJjyzrF-Xi",
        "colab_type": "code",
        "outputId": "79f30b89-2780-48ee-b30a-deaafb5894a9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 337
        }
      },
      "source": [
        "train_df.describe()"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>date</th>\n",
              "      <th>visitId</th>\n",
              "      <th>visitNumber</th>\n",
              "      <th>visitStartTime</th>\n",
              "      <th>totals.bounces</th>\n",
              "      <th>totals.hits</th>\n",
              "      <th>totals.newVisits</th>\n",
              "      <th>totals.pageviews</th>\n",
              "      <th>totals.sessionQualityDim</th>\n",
              "      <th>totals.timeOnSite</th>\n",
              "      <th>totals.totalTransactionRevenue</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "      <th>totals.transactions</th>\n",
              "      <th>totals.visits</th>\n",
              "      <th>trafficSource.adwordsClickInfo.page</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>count</th>\n",
              "      <td>2.000000e+04</td>\n",
              "      <td>2.000000e+04</td>\n",
              "      <td>20000.000000</td>\n",
              "      <td>2.000000e+04</td>\n",
              "      <td>9873.0</td>\n",
              "      <td>20000.000000</td>\n",
              "      <td>15088.0</td>\n",
              "      <td>19999.000000</td>\n",
              "      <td>9120.000000</td>\n",
              "      <td>10101.000000</td>\n",
              "      <td>1.930000e+02</td>\n",
              "      <td>1.930000e+02</td>\n",
              "      <td>196.000000</td>\n",
              "      <td>20000.0</td>\n",
              "      <td>630.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>mean</th>\n",
              "      <td>2.017041e+07</td>\n",
              "      <td>1.498277e+09</td>\n",
              "      <td>2.264200</td>\n",
              "      <td>1.498277e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>4.794450</td>\n",
              "      <td>1.0</td>\n",
              "      <td>3.971549</td>\n",
              "      <td>4.456140</td>\n",
              "      <td>264.244629</td>\n",
              "      <td>1.278192e+08</td>\n",
              "      <td>1.087636e+08</td>\n",
              "      <td>1.040816</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.023810</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>std</th>\n",
              "      <td>4.737638e+03</td>\n",
              "      <td>1.565797e+07</td>\n",
              "      <td>7.876636</td>\n",
              "      <td>1.565797e+07</td>\n",
              "      <td>0.0</td>\n",
              "      <td>9.080243</td>\n",
              "      <td>0.0</td>\n",
              "      <td>6.498605</td>\n",
              "      <td>12.593541</td>\n",
              "      <td>459.176173</td>\n",
              "      <td>2.432262e+08</td>\n",
              "      <td>1.711924e+08</td>\n",
              "      <td>0.222727</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.172159</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>min</th>\n",
              "      <td>2.016090e+07</td>\n",
              "      <td>1.472799e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.472800e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>4.990000e+06</td>\n",
              "      <td>1.990000e+06</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>25%</th>\n",
              "      <td>2.017020e+07</td>\n",
              "      <td>1.486118e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.486118e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>35.000000</td>\n",
              "      <td>2.799000e+07</td>\n",
              "      <td>2.102000e+07</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>50%</th>\n",
              "      <td>2.017062e+07</td>\n",
              "      <td>1.498247e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.498247e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>2.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>2.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>94.000000</td>\n",
              "      <td>5.171000e+07</td>\n",
              "      <td>4.458000e+07</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>75%</th>\n",
              "      <td>2.017113e+07</td>\n",
              "      <td>1.512038e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.512038e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>5.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>4.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>270.000000</td>\n",
              "      <td>1.141600e+08</td>\n",
              "      <td>1.087200e+08</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>max</th>\n",
              "      <td>2.018042e+07</td>\n",
              "      <td>1.523862e+09</td>\n",
              "      <td>401.000000</td>\n",
              "      <td>1.523862e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>229.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>165.000000</td>\n",
              "      <td>96.000000</td>\n",
              "      <td>5553.000000</td>\n",
              "      <td>2.103690e+09</td>\n",
              "      <td>1.171470e+09</td>\n",
              "      <td>3.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>3.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "               date  ...  trafficSource.adwordsClickInfo.page\n",
              "count  2.000000e+04  ...                           630.000000\n",
              "mean   2.017041e+07  ...                             1.023810\n",
              "std    4.737638e+03  ...                             0.172159\n",
              "min    2.016090e+07  ...                             1.000000\n",
              "25%    2.017020e+07  ...                             1.000000\n",
              "50%    2.017062e+07  ...                             1.000000\n",
              "75%    2.017113e+07  ...                             1.000000\n",
              "max    2.018042e+07  ...                             3.000000\n",
              "\n",
              "[8 rows x 15 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 61
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "n7dc9a8HeKUD",
        "colab_type": "code",
        "outputId": "a388568a-6f21-4e86-b2e2-6c455c6b4d14",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 119
        }
      },
      "source": [
        "train_df['date'].head()"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0    20171016\n",
              "1    20171016\n",
              "2    20171016\n",
              "3    20171016\n",
              "4    20171016\n",
              "Name: date, dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 62
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "ZjAuXXzNCJrq",
        "colab_type": "code",
        "outputId": "5f8aa39b-c3d4-4ae7-9124-2c9e75c550e5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 102
        }
      },
      "source": [
        "#------------------------------------------------------------------------------------------------\n",
        "# TESTING DATAFRAME - REMOVING EMPTY COLUMNS with value \"not available in demo dataset\"\n",
        "#------------------------------------------------------------------------------------------------\n",
        "test_df = removeUselessColumns(test_df)\n"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "DATAFRAME IS 59 COLUMNS...\n",
            "FOUND 0 USELESS COLUMNS...\n",
            "COLUMNS:  []\n",
            "REMOVING 0 COLUMNS...\n",
            "DATAFRAME IS NOW 59 COLUMNS...\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "iFjbxvn2EIkf",
        "colab_type": "code",
        "outputId": "b7fa95fb-de3b-4b55-a639-1a0389b0c6ae",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 414
        }
      },
      "source": [
        "test_df.head(5)"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>channelGrouping</th>\n",
              "      <th>customDimensions</th>\n",
              "      <th>date</th>\n",
              "      <th>fullVisitorId</th>\n",
              "      <th>hits</th>\n",
              "      <th>socialEngagementType</th>\n",
              "      <th>visitId</th>\n",
              "      <th>visitNumber</th>\n",
              "      <th>visitStartTime</th>\n",
              "      <th>device.browser</th>\n",
              "      <th>device.browserSize</th>\n",
              "      <th>device.browserVersion</th>\n",
              "      <th>device.deviceCategory</th>\n",
              "      <th>device.flashVersion</th>\n",
              "      <th>device.isMobile</th>\n",
              "      <th>device.language</th>\n",
              "      <th>device.mobileDeviceBranding</th>\n",
              "      <th>device.mobileDeviceInfo</th>\n",
              "      <th>device.mobileDeviceMarketingName</th>\n",
              "      <th>device.mobileDeviceModel</th>\n",
              "      <th>device.mobileInputSelector</th>\n",
              "      <th>device.operatingSystem</th>\n",
              "      <th>device.operatingSystemVersion</th>\n",
              "      <th>device.screenColors</th>\n",
              "      <th>device.screenResolution</th>\n",
              "      <th>geoNetwork.city</th>\n",
              "      <th>geoNetwork.cityId</th>\n",
              "      <th>geoNetwork.continent</th>\n",
              "      <th>geoNetwork.country</th>\n",
              "      <th>geoNetwork.latitude</th>\n",
              "      <th>geoNetwork.longitude</th>\n",
              "      <th>geoNetwork.metro</th>\n",
              "      <th>geoNetwork.networkDomain</th>\n",
              "      <th>geoNetwork.networkLocation</th>\n",
              "      <th>geoNetwork.region</th>\n",
              "      <th>geoNetwork.subContinent</th>\n",
              "      <th>totals.bounces</th>\n",
              "      <th>totals.hits</th>\n",
              "      <th>totals.newVisits</th>\n",
              "      <th>totals.pageviews</th>\n",
              "      <th>totals.sessionQualityDim</th>\n",
              "      <th>totals.timeOnSite</th>\n",
              "      <th>totals.totalTransactionRevenue</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "      <th>totals.transactions</th>\n",
              "      <th>totals.visits</th>\n",
              "      <th>trafficSource.adContent</th>\n",
              "      <th>trafficSource.adwordsClickInfo.adNetworkType</th>\n",
              "      <th>trafficSource.adwordsClickInfo.criteriaParameters</th>\n",
              "      <th>trafficSource.adwordsClickInfo.gclId</th>\n",
              "      <th>trafficSource.adwordsClickInfo.isVideoAd</th>\n",
              "      <th>trafficSource.adwordsClickInfo.page</th>\n",
              "      <th>trafficSource.adwordsClickInfo.slot</th>\n",
              "      <th>trafficSource.campaign</th>\n",
              "      <th>trafficSource.isTrueDirect</th>\n",
              "      <th>trafficSource.keyword</th>\n",
              "      <th>trafficSource.medium</th>\n",
              "      <th>trafficSource.referralPath</th>\n",
              "      <th>trafficSource.source</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'APAC'}]</td>\n",
              "      <td>20180511</td>\n",
              "      <td>7460955084541987166</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '21',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1526099341</td>\n",
              "      <td>2</td>\n",
              "      <td>1526099341</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>mobile</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>True</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Android</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Asia</td>\n",
              "      <td>India</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>unknown.unknown</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Delhi</td>\n",
              "      <td>Southern Asia</td>\n",
              "      <td>NaN</td>\n",
              "      <td>4</td>\n",
              "      <td>NaN</td>\n",
              "      <td>3.0</td>\n",
              "      <td>1</td>\n",
              "      <td>973.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>True</td>\n",
              "      <td>(not provided)</td>\n",
              "      <td>organic</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Direct</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20180511</td>\n",
              "      <td>460252456180441002</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '11',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1526064483</td>\n",
              "      <td>166</td>\n",
              "      <td>1526064483</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>desktop</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>False</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Macintosh</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>San Francisco</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>San Francisco-Oakland-San Jose CA</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>California</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>4</td>\n",
              "      <td>NaN</td>\n",
              "      <td>3.0</td>\n",
              "      <td>1</td>\n",
              "      <td>49.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>True</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>(none)</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>(direct)</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20180511</td>\n",
              "      <td>3461808543879602873</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '12',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1526067157</td>\n",
              "      <td>2</td>\n",
              "      <td>1526067157</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>desktop</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>False</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Chrome OS</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>onlinecomputerworks.com</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>4</td>\n",
              "      <td>NaN</td>\n",
              "      <td>3.0</td>\n",
              "      <td>1</td>\n",
              "      <td>24.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>True</td>\n",
              "      <td>(not provided)</td>\n",
              "      <td>organic</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Direct</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20180511</td>\n",
              "      <td>975129477712150630</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '23',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1526107551</td>\n",
              "      <td>4</td>\n",
              "      <td>1526107551</td>\n",
              "      <td>Chrome</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>mobile</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>True</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>iOS</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Houston</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Houston TX</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Texas</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>5</td>\n",
              "      <td>NaN</td>\n",
              "      <td>4.0</td>\n",
              "      <td>1</td>\n",
              "      <td>25.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>True</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>(none)</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>(direct)</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Organic Search</td>\n",
              "      <td>[{'index': '4', 'value': 'North America'}]</td>\n",
              "      <td>20180511</td>\n",
              "      <td>8381672768065729990</td>\n",
              "      <td>[{'hitNumber': '1', 'time': '0', 'hour': '10',...</td>\n",
              "      <td>Not Socially Engaged</td>\n",
              "      <td>1526060254</td>\n",
              "      <td>1</td>\n",
              "      <td>1526060254</td>\n",
              "      <td>Internet Explorer</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>tablet</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>True</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Windows</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Irvine</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Americas</td>\n",
              "      <td>United States</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>Los Angeles CA</td>\n",
              "      <td>com</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>California</td>\n",
              "      <td>Northern America</td>\n",
              "      <td>NaN</td>\n",
              "      <td>5</td>\n",
              "      <td>1.0</td>\n",
              "      <td>4.0</td>\n",
              "      <td>1</td>\n",
              "      <td>49.0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>1</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>not available in demo dataset</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>NaN</td>\n",
              "      <td>(not provided)</td>\n",
              "      <td>organic</td>\n",
              "      <td>(not set)</td>\n",
              "      <td>google</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "  channelGrouping  ... trafficSource.source\n",
              "0  Organic Search  ...               google\n",
              "1          Direct  ...             (direct)\n",
              "2  Organic Search  ...               google\n",
              "3          Direct  ...             (direct)\n",
              "4  Organic Search  ...               google\n",
              "\n",
              "[5 rows x 59 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 64
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "S9eu2vlJENyw",
        "colab_type": "code",
        "outputId": "aee67837-7db9-460c-bed1-2f1aac70b2b5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 337
        }
      },
      "source": [
        "test_df.describe()"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>date</th>\n",
              "      <th>visitId</th>\n",
              "      <th>visitNumber</th>\n",
              "      <th>visitStartTime</th>\n",
              "      <th>totals.bounces</th>\n",
              "      <th>totals.hits</th>\n",
              "      <th>totals.newVisits</th>\n",
              "      <th>totals.pageviews</th>\n",
              "      <th>totals.sessionQualityDim</th>\n",
              "      <th>totals.timeOnSite</th>\n",
              "      <th>totals.totalTransactionRevenue</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "      <th>totals.transactions</th>\n",
              "      <th>totals.visits</th>\n",
              "      <th>trafficSource.adwordsClickInfo.page</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>count</th>\n",
              "      <td>2000.0</td>\n",
              "      <td>2.000000e+03</td>\n",
              "      <td>2000.000000</td>\n",
              "      <td>2.000000e+03</td>\n",
              "      <td>1400.0</td>\n",
              "      <td>2000.000000</td>\n",
              "      <td>1444.0</td>\n",
              "      <td>1999.000000</td>\n",
              "      <td>2000.000000</td>\n",
              "      <td>597.000000</td>\n",
              "      <td>3.100000e+01</td>\n",
              "      <td>3.100000e+01</td>\n",
              "      <td>31.0</td>\n",
              "      <td>2000.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>mean</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526062e+09</td>\n",
              "      <td>2.586000</td>\n",
              "      <td>1.526062e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>5.063500</td>\n",
              "      <td>1.0</td>\n",
              "      <td>3.865433</td>\n",
              "      <td>5.054000</td>\n",
              "      <td>356.514238</td>\n",
              "      <td>1.566197e+08</td>\n",
              "      <td>1.520068e+08</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>std</th>\n",
              "      <td>0.0</td>\n",
              "      <td>2.185853e+04</td>\n",
              "      <td>9.711424</td>\n",
              "      <td>2.185514e+04</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.766749</td>\n",
              "      <td>0.0</td>\n",
              "      <td>6.237893</td>\n",
              "      <td>13.764658</td>\n",
              "      <td>527.043185</td>\n",
              "      <td>2.389345e+08</td>\n",
              "      <td>2.385346e+08</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>min</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526021e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.526022e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>3.750000e+06</td>\n",
              "      <td>1.750000e+06</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>25%</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526045e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.526045e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>74.000000</td>\n",
              "      <td>2.509000e+07</td>\n",
              "      <td>2.138500e+07</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>50%</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526060e+09</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.526060e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>168.000000</td>\n",
              "      <td>5.597000e+07</td>\n",
              "      <td>5.097000e+07</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>75%</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526078e+09</td>\n",
              "      <td>2.000000</td>\n",
              "      <td>1.526078e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>6.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>4.000000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>390.000000</td>\n",
              "      <td>1.344700e+08</td>\n",
              "      <td>1.309700e+08</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>max</th>\n",
              "      <td>20180511.0</td>\n",
              "      <td>1.526108e+09</td>\n",
              "      <td>195.000000</td>\n",
              "      <td>1.526108e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>87.000000</td>\n",
              "      <td>1.0</td>\n",
              "      <td>67.000000</td>\n",
              "      <td>94.000000</td>\n",
              "      <td>5268.000000</td>\n",
              "      <td>1.082500e+09</td>\n",
              "      <td>1.076500e+09</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "             date  ...  trafficSource.adwordsClickInfo.page\n",
              "count      2000.0  ...                                  3.0\n",
              "mean   20180511.0  ...                                  1.0\n",
              "std           0.0  ...                                  0.0\n",
              "min    20180511.0  ...                                  1.0\n",
              "25%    20180511.0  ...                                  1.0\n",
              "50%    20180511.0  ...                                  1.0\n",
              "75%    20180511.0  ...                                  1.0\n",
              "max    20180511.0  ...                                  1.0\n",
              "\n",
              "[8 rows x 15 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 65
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "PcT43DABT7_6",
        "colab_type": "text"
      },
      "source": [
        "**Impute 0 for ALL missing target values (totals.transactionRevenue)**"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "zeleDYJTHH16",
        "colab_type": "text"
      },
      "source": [
        "## Check Missing Data"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "G87kpIOaHbAd",
        "colab_type": "code",
        "outputId": "3dee3210-c763-485e-99be-7af37c56d713",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 306
        }
      },
      "source": [
        "# checking missing data\n",
        "miss_per = {}\n",
        "for k, v in dict(train_df.isna().sum(axis=0)).items():\n",
        "    if v == 0:\n",
        "        continue\n",
        "    miss_per[k] = 100 * float(v) / len(train_df)\n",
        "miss_per"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'totals.bounces': 50.635,\n",
              " 'totals.newVisits': 24.56,\n",
              " 'totals.pageviews': 0.005,\n",
              " 'totals.sessionQualityDim': 54.4,\n",
              " 'totals.timeOnSite': 49.495,\n",
              " 'totals.totalTransactionRevenue': 99.035,\n",
              " 'totals.transactionRevenue': 99.035,\n",
              " 'totals.transactions': 99.02,\n",
              " 'trafficSource.adContent': 97.395,\n",
              " 'trafficSource.adwordsClickInfo.adNetworkType': 96.85,\n",
              " 'trafficSource.adwordsClickInfo.gclId': 96.835,\n",
              " 'trafficSource.adwordsClickInfo.isVideoAd': 96.85,\n",
              " 'trafficSource.adwordsClickInfo.page': 96.85,\n",
              " 'trafficSource.adwordsClickInfo.slot': 96.85,\n",
              " 'trafficSource.isTrueDirect': 68.335,\n",
              " 'trafficSource.keyword': 66.05,\n",
              " 'trafficSource.referralPath': 69.48}"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 66
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0un1MrwyUOvu",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "#train_df[\"totals.transactionRevenue\"].fillna(0, inplace=True)\n",
        "#test_df[\"totals.transactionRevenue\"].fillna(0, inplace=True)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "pWM7iHTyX9pV",
        "colab_type": "text"
      },
      "source": [
        "**Remove columns that are in TRAINING which are not there in TEST**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "dd44J7YCYKU0",
        "colab_type": "code",
        "outputId": "d2678811-88dd-4d52-ab61-9c4b3b3c2146",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "print(\"Columns not in TEST but in TRAIN : \", set(train_df.columns).difference(set(test_df.columns)))"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Columns not in TEST but in TRAIN :  set()\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "go1wEnjaTjQo"
      },
      "source": [
        "# **3 - MODELING & EVALUTATION**\n",
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "egPQKGV4Ah8B",
        "colab_type": "text"
      },
      "source": [
        " \n",
        " \n",
        "Since we are predicting the natural log of sum of all transactions of the user, let us sum up the transaction revenue at user level and take a log and then do a scatter plot.\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "u_BWXJJ4QFNq",
        "colab_type": "text"
      },
      "source": [
        "First we have to change the datatype to 'FLOAT' to make sure the value is a dollar value"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "80ejCkQSJhIh",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_df[\"totals.transactionRevenue\"] = train_df[\"totals.transactionRevenue\"].astype('float')"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mmAh-mjOQo_x",
        "colab_type": "text"
      },
      "source": [
        "Next we have to group the USER level transaction to by using the GROUPBY function on the dataframe. This will give us the Total Transaction Value for given user. "
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "2DQId6KsRBQS",
        "colab_type": "code",
        "outputId": "60ac40ca-4e35-4289-d104-95fb9704e537",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 419
        }
      },
      "source": [
        "grouped_df_sum = train_df.groupby(\"fullVisitorId\")[\"totals.transactionRevenue\"].sum().reset_index()\n",
        "grouped_df_sum.sort_values(by=['totals.transactionRevenue'], inplace=True, ascending=False)\n",
        "grouped_df_sum"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>fullVisitorId</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>3257</th>\n",
              "      <td>1814166460229302850</td>\n",
              "      <td>1.171470e+09</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14060</th>\n",
              "      <td>7638336411447332495</td>\n",
              "      <td>1.077000e+09</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5602</th>\n",
              "      <td>309482894121265066</td>\n",
              "      <td>9.004300e+08</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5704</th>\n",
              "      <td>3152246617474456269</td>\n",
              "      <td>6.355000e+08</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13149</th>\n",
              "      <td>7168226225550508027</td>\n",
              "      <td>5.939100e+08</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6163</th>\n",
              "      <td>3396397804735366613</td>\n",
              "      <td>0.000000e+00</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6164</th>\n",
              "      <td>3396461882036302761</td>\n",
              "      <td>0.000000e+00</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6165</th>\n",
              "      <td>3396775680310832137</td>\n",
              "      <td>0.000000e+00</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6166</th>\n",
              "      <td>3398101758099870675</td>\n",
              "      <td>0.000000e+00</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18383</th>\n",
              "      <td>9999250019952621738</td>\n",
              "      <td>0.000000e+00</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>18384 rows × 2 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "             fullVisitorId  totals.transactionRevenue\n",
              "3257   1814166460229302850               1.171470e+09\n",
              "14060  7638336411447332495               1.077000e+09\n",
              "5602    309482894121265066               9.004300e+08\n",
              "5704   3152246617474456269               6.355000e+08\n",
              "13149  7168226225550508027               5.939100e+08\n",
              "...                    ...                        ...\n",
              "6163   3396397804735366613               0.000000e+00\n",
              "6164   3396461882036302761               0.000000e+00\n",
              "6165   3396775680310832137               0.000000e+00\n",
              "6166   3398101758099870675               0.000000e+00\n",
              "18383  9999250019952621738               0.000000e+00\n",
              "\n",
              "[18384 rows x 2 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 73
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "T_TKLoAC6FRc",
        "colab_type": "code",
        "outputId": "89ac8098-7e3d-4c41-e731-708e0c2e02f2",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 516
        }
      },
      "source": [
        "ax = grouped_df_sum.hist('totals.transactionRevenue', bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)\n",
        "ax = ax[0]\n",
        "for x in ax:\n",
        "\n",
        "    # Despine\n",
        "    x.spines['right'].set_visible(False)\n",
        "    x.spines['top'].set_visible(False)\n",
        "    x.spines['left'].set_visible(False)\n",
        "\n",
        "    # Switch off ticks\n",
        "    x.tick_params(axis=\"both\", which=\"both\", bottom=\"off\", top=\"off\", labelbottom=\"on\", left=\"off\", right=\"off\", labelleft=\"on\")\n",
        "\n",
        "    # Draw horizontal axis lines\n",
        "    vals = x.get_yticks()\n",
        "    for tick in vals:\n",
        "        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)\n",
        "\n",
        "    # Remove title\n",
        "    x.set_title(\"\")\n",
        "\n",
        "    # Set x-axis label\n",
        "    x.set_xlabel(\"Total Transaction Revenue (per User)\", labelpad=20, weight='bold', size=12)\n",
        "\n",
        "    # Set y-axis label\n",
        "    x.set_ylabel(\"Visitors\", labelpad=20, weight='bold', size=14)\n",
        "\n"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAAvQAAAHzCAYAAABPMYkzAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0\ndHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nO3debhlVX3u+++7m1JjE1GUIDYQgw2i\nYnPVJCex7NFzEtQYhZsIKLGMEZsbTYQkJ3L1GDSJMSFRo5YIJCeg0RjrEpUgETUqSqlIp0iJokUQ\nG1A80bi73/1jzg2rdu1mQdXae4+q7+d51rPWGmM2Y605Ct459phzpaqQJEmS1KaxtW6AJEmSpFvP\nQC9JkiQ1zEAvSZIkNcxA36Akm9a6DVqax2f98xitbx6f9c3js/55jNa3URwfA32b/Ie6vnl81j+P\n0frm8VnfPD7rn8dofTPQS5IkSbrZxFo3YA+w6vf9fNvb3rYm+9VwPD7rn8doffP4rG8en/XPY7S+\n7cLxyZIV3od+l/kFSpIkadSWDPROuZEkSZIaZqCXJEmSGmaglyRJkhpmoJckSZIaZqCXJEmSGmag\nlyRJkhpmoJckSZIaZqCXJEmSGmaglyRJkhpmoJckSZIaZqCXJEmSGmaglyRJkhpmoJckSZIaZqCX\nJEmSGmaglyRJkhrWTKBPcq8kH01yeZLLkrysL79LknOTXNk/79OXJ8kpSbYluTjJwwe2dUy//JVJ\njhkof0SSS/p1TkmS1f+kkiRJ0vCaCfTADPCKqjoEeAzw4iSHACcA51XVwcB5/XuApwIH949NwFuh\nOwEAXg08GngU8Or5k4B+mRcMrHf4KnwuSZIk6VZrJtBX1bVV9fn+9Q+BLwEHAEcAp/eLnQ48vX99\nBHBGdS4A7pxkf+ApwLlVdX1V3QCcCxze192pqi6oqgLOGNiWJEmStC5NrHUDbo0kBwIPAz4D7FdV\n1/ZV3wL2618fAHxzYLXtfdly5dsXKV/W1NTUTmXj4+OMj49TVUxPT4+sfm5ujpmZmZ3qJyYmGBsb\nG3n97Owss7OzO9VPTk6SZGT1GzZsAGBmZoa5ubkd6pIwOTm5KvXT09N05343GxsbY2JiYlXq7Xv2\nvUH2PfveatTb9+x7g+x7q9v35o/FYpoZoZ+X5A7A+4CXV9WNg3X9yHotuuLubcOmJFuTbN28efOo\ndydJkqS93GD+7B+bbqpbeDayniWZBM4Gzqmqv+jLrgA2VtW1/bSZ86vq/kne1r8+c3C5+UdVvbAv\nfxtwfv/4aFU9oC8/anC5ZbTzBUqSJKlVS96spZkR+v6OM+8EvjQf5ntbgPk71RwDfGCg/Oj+bjeP\nAX7QT805B3hykn36i2GfTHeCcC1wY5LH9Ps6emBbkiRJ0rrUzAh9kv8GfAK4BJifZPUHdPPo3wPc\nG7gaeHZVXd+H8r+hu1PNj4DnVdXWflvP79cFeF1VvasvfyRwGnA74EPAS2rlL6iNL1CSJEktW3KE\nvplAv475BUqSJGnU2p9yI0mSJGlnBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWEG\nekmSJKlhBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6\nSZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJ\nkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWEGekmSJKlhBnpJkiSpYQZ6SZIkqWETa90A\n3Tonn3/KSLZ74saXjmS7kiRJGg1H6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhno\nJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIY1E+iTnJrk20ku\nHSh7d5KL+sfXk1zUlx+Y5McDdX87sM4jklySZFuSU5KkL79LknOTXNk/77P6n1KSJEm6ZZoJ9MBp\nwOGDBVX1nKo6rKoOA94H/NNA9Vfn66rqtwfK3wq8ADi4f8xv8wTgvKo6GDivfy9JkiStaxNr3YBh\nVdXHkxy4WF0/yv5s4PHLbSPJ/sCdquqC/v0ZwNOBDwFHABv7RU8HzgdetVK7pqamdiobHx9nfHyc\nqmJ6enok9aMyNTXFxMQEY2NjzM3NMTMzs9My8/Wzs7PMzs7uVD85OUmSkdVv2LABgJmZGebm5nao\nS8Lk5OSq1E9PT1NVO9SPjY0xMTGxKvVr1ffGx8dX7Bujrrfv2fcWsu/Z9+x79r09ve/NH4vFtDRC\nv5xfAq6rqisHyg5K8oUkH0vyS33ZAcD2gWW292UA+1XVtf3rbwH7LbWzJJuSbE2ydfPmzbvpI0iS\nJEmLG8yf/WPTTXULz0bWs36E/uyqOnRB+VuBbVX1xv79bYA7VNX3kjwC+GfgQcD9gNdX1RP75X4J\neFVV/Y8k36+qOw9s84aqGmYe/Zp8gSeff8pItnvixpeOZLuSJEnaJVmqopkpN0tJMgE8E3jEfFlV\n/QT4Sf/6c0m+ShfmrwHuObD6PfsygOuS7F9V1/ZTc769Gu2XJEmSdsWeMOXmicCXq+qmqTRJ7pZk\nvH/9s3QXv17VT6m5Mclj+nn3RwMf6FfbAhzTvz5moFySJElat5oJ9EnOBD4N3D/J9iTH9VVHAmcu\nWPyXgYv721i+F/jtqrq+r/sdYDOwDfgq3QWxAK8HnpTkSrqThNeP7MNIkiRJu0kzU26q6qglyo9d\npOx9dLexXGz5rcChi5R/D3jCrrVSkiRJWl3NjNBLkiRJ2pmBXpIkSWqYgV6SJElqmIFekiRJapiB\nXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFe\nkiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6S\nJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIk\nSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqmIFekiRJ\napiBXpIkSWqYgV6SJElqmIFekiRJapiBXpIkSWqYgV6SJElqWDOBPsmpSb6d5NKBspOSXJPkov7x\ntIG6E5NsS3JFkqcMlB/el21LcsJA+UFJPtOXvzvJhtX7dJIkSdKt00ygB04DDl+k/E1VdVj/+CBA\nkkOAI4EH9eu8Jcl4knHgzcBTgUOAo/plAd7Qb+vngBuA40b6aSRJkqTdoJlAX1UfB64fcvEjgLOq\n6idV9TVgG/Co/rGtqq6qqingLOCIJAEeD7y3X/904Om79QNIkiRJIzCx1g3YDY5PcjSwFXhFVd0A\nHABcMLDM9r4M4JsLyh8N3BX4flXNLLL8sqampnYqGx8fZ3x8nKpienp6JPWjMjU1xcTEBGNjY8zN\nzTEzM7PTMvP1s7OzzM7O7lQ/OTlJkpHVb9jQzYaamZlhbm5uh7okTE5Orkr99PQ0VbVD/djYGBMT\nE6tSv1Z9b3x8fMW+Mep6+559byH7nn3Pvmff29P73vyxWEwzI/RLeCtwX+Aw4Frgjaux0ySbkmxN\nsnXz5s2rsUtJkiTtxQbzZ//YdFPdwrOR9SzJgcDZVXXocnVJTgSoqpP7unOAk/pFT6qqp/TlJ/Zl\nrwe+A/xMVc0k+fnB5VawJl/gyeefMpLtnrjxpSPZriRJknZJlqpoeoQ+yf4Db58BzN8BZwtwZJLb\nJDkIOBj4LHAhcHB/R5sNdBfObqnurOajwLP69Y8BPrAan0GSJEnaFc3MoU9yJrAR2DfJduDVwMYk\nh9GNkn8deCFAVV2W5D3A5cAM8OKqmu23czxwDjAOnFpVl/W7eBVwVpL/BXwBeOcqfTRJkiTpVmtq\nys065ZQbSZIkjdqeOeVGkiRJ2tsZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhno\nJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGegl\nSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJ\nkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmS\npIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKk\nhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIY1E+iTnJrk20kuHSj7syRfTnJxkvcnuXNffmCS\nHye5qH/87cA6j0hySZJtSU5Jkr78LknOTXJl/7zP6n9KSZIk6ZZpJtADpwGHLyg7Fzi0qh4CfAU4\ncaDuq1V1WP/47YHytwIvAA7uH/PbPAE4r6oOBs7r30uSJEnrWjOBvqo+Dly/oOxfq2qmf3sBcM/l\ntpFkf+BOVXVBVRVwBvD0vvoI4PT+9ekD5ZIkSdK6NbHWDdiNng+8e+D9QUm+ANwI/FFVfQI4ANg+\nsMz2vgxgv6q6tn/9LWC/YXY6NTW1U9n4+Djj4+NUFdPT0yOpH5WpqSkmJiYYGxtjbm6OmZmZnZaZ\nr5+dnWV2dnan+snJSZKMrH7Dhg0AzMzMMDc3t0NdEiYnJ1elfnp6mu688GZjY2NMTEysSv1a9b3x\n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\nc/q6G5M8pr+7zdED25IkSZLWpWF/KfYa4NAk76Cbo/7FvvxuwLdH0bDFJDmTboR93yTb6e5W83rg\nPUmOo7uN5rP7xT8IPA3YBvwIeB5AVV2f5LXAhf1yr6mq+Qttf4fuTjq3Az7UPyRJkqR1a9hA/27g\nD+h+QGoO+Mck96CbV/8vI2rbTqrqqCWqnrDIsgW8eIntnAqcukj5VuDQXWmjJEmStJqGDfR/DFxH\nd2/2s6vq4iQPpvsV2Y+NqnGSJEmSljdUoK+qOeCvF5RdQndRrCRJkqQ1smSgT/LHwPaqOrV/vaSq\nes1ub5kkSZKkFS03Qn8S8Gm6ueYnsfztGQ30kiRJ0hpYacpNlngtSZIkaR1Y8j70VTUGbE3y0Koa\nW+6xiu2VJEmSNGClMH488Pkkn0/ykiSr9ouwkiRJkla2UqCfoZtqcxjwl8A1Sd6X5H8kcWRekiRJ\nWmMrhfL9gZcBW+mC/Qbg6cAHgO1J3pDkkNE2UZIkSdJSlg30VfW9qvrrqnoUcAjwBmA7Xbj/GeCV\nwMUjb6UkSZKkRQ09baaqvlxVJ1bVfYCjgR/SBXvvfiNJkiStkaF+KRYgye2AXwOeCzyeW3AyIEmS\nJGk0Vgz0SR5PNyL/TOD288XAHHAu8K6RtU6SJEnSspYN9Em+ARww/7Z/3gacBpxRVdtH1zRJkiRJ\nK1lphP6e/fP/Ad4DvKuqPjnaJkmSJEka1kqB/mN0U2reW1U/WoX2SJIkSboFlg30VfW41WqIJEmS\npFvOO9VIkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5Ik\nSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJ\nDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkN\nM9BLkiRJDTPQS5IkSQ1rPtAnuX+SiwYeNyZ5eZKTklwzUP60gXVOTLItyRVJnjJQfnhfti3JCWvz\niSRJkqThTax1A3ZVVV0BHAaQZBy4Bng/8DzgTVX154PLJzkEOBJ4EHAP4CNJ7tdXvxl4ErAduDDJ\nlqq6fFU+iCRJknQrNB/oF3gC8NWqujrJUsscAZxVVT8BvpZkG/Covm5bVV0FkOSsftllA/3U1NRO\nZePj44yPj1NVTE9Pj6R+VKamppiYmGBsbIy5uTlmZmZ2Wma+fnZ2ltnZ2Z3qJycnSTKy+g0bNgAw\nMzPD3NzcDnVJmJycXJX66elpqmqH+rGxMSYmJlalfq363vj4+Ip9Y9T19j373kL2Pfuefc++t6f3\nvfljsZjmp9wscCRw5sD745NcnOTUJPv0ZQcA3xxYZntftlT5TpJsSrI1ydbNmzfvvtZLkiRJixjM\nn/1j0011C89GWpVkA/AfwIOq6rok+wHfBQp4LbB/VT0/yd8AF1TV3/frvRP4UL+Zw6vqt/ry5wKP\nrqrjV9j1mnyBJ59/yki2e+LGl45ku5IkSdolS04/2ZOm3DwV+HxVXQcw/wyQ5B3A2f3ba4B7Dax3\nz76MZcolSZKkdWlPmnJzFAPTbZLsP1D3DODS/vUW4Mgkt0lyEHAw8FngQuDgJAf1o/1H9stKkiRJ\n69YeMUKf5PZ0d6d54UDxnyY5jG5KzNfn66rqsiTvobvYdQZ4cVXN9ts5HjgHGAdOrarLVu1DSJIk\nSbfCHhHoq+o/gbsuKHvuMsu/DnjdIuUfBD642xsoSZIkjcieNOVGkiRJ2usY6CVJkqSGGeglSZKk\nhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSG\nGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ\n6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhno\nJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGegl\nSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIYZ6CVJkqSGGeglSZKkhhnoJUmSpIbtMYE+\nydeTXJLkoiRb+7K7JDk3yZX98z59eZKckmRbkouTPHxgO8f0y1+Z5Ji1+jySJEnSMPaYQN97XFUd\nVlWP7N+fAJxXVQcD5/XvAZ4KHNw/NgFvhe4EAHg18GjgUcCr508CJEmSpPVoYq0bMGJHABv716cD\n5wOv6svPqKoCLkhy5yT798ueW1XXAyQ5FzgcOHOpHUxNTe1UNj4+zvj4OFXF9PT0SOpHZWpqiomJ\nCcbGxpibm2NmZmanZebrZ2dnmZ2d3al+cnKSJCOr37BhAwAzMzPMzc3tUJeEycnJVamfnp6m60I3\nGxsbY2JiYlXq16rvjY+Pr9g3Rl1v37PvLWTfs+/Z9+x7e3rfmz8Wi9mTRugL+Nckn0uyqS/br6qu\n7V9/C9ivf30A8M2Bdbf3ZUuV7yDJpiRbk2zdvHnz7vwMkiRJ0k4G82f/2HRT3cKzkVYlOaCqrkly\nd+Bc4CXAlqq688AyN1TVPknOBl5fVf/el59HN3K/EbhtVf2vvvx/Aj+uqj9fZtdr8gWefP4pI9nu\niRtfOpLtSpIkaZdkqYo9ZoS+qq7pn78NvJ9uDvx1/VQa+udv94tfA9xrYPV79mVLlUuSJEnr0h4R\n6JPcPskd518DTwYuBbYA83eqOQb4QP96C3B0f7ebxwA/6KfmnAM8Ock+/cWwT+7LJEmSpHVpT7ko\ndj/g/Umg+0z/UFUfTnIh8J4kxwFXA8/ul/8g8DRgG/Aj4HkAVXV9ktcCF/bLvWb+AllJkiRpPdoj\nAn1VXQU8dJHy7wFPWKS8gBcvsa1TgVN3dxslSZKkUdgjptxIkiRJeysDvSRJktQwA70kSZLUMAO9\nJEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70k\nSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJ\nktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS\n1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLU\nMAO9JEmS1DADvSRJktQwA70kSZLUMAO9JEmS1DADvSRJktQwA70kSZLUsOYDfZJ7JfloksuTXJbk\nZX35SUmuSXJR/3jawDonJtmW5IokTxkoP7wv25bkhLX4PJIkSdItMbHWDdgNZoBXVNXnk9wR+FyS\nc/u6N1XVnw8unOQQ4EjgQcA9gI8kuV9f/WbgScB24MIkW6rq8lX5FJIkSdKt0Hygr6prgWv71z9M\n8iXggGVWOQI4q6p+AnwtyTbgUX3dtqq6CiDJWf2yBnpJkiStW80H+kFJDgQeBnwG+EXg+CRHA1vp\nRvFvoAv7Fwystp2bTwC+uaD80Svtc2pqaqey8fFxxsfHqSqmp6dHUj8qU1NTTExMMDY2xtzcHDMz\nMzstM18/OzvL7OzsTvWTk5MkGVn9hg0bAJiZmWFubm6HuiRMTk6uSv309DRVtUP92NgYExMTq1K/\nVn1vfHx8xb4x6nr7nn1vIfrqBuIAABMwSURBVPuefc++Z9/b0/ve/LFYTPNz6OcluQPwPuDlVXUj\n8FbgvsBhdCP4b9yN+9qUZGuSrZs3b95dm5UkSZIWNZg/+8emm+oWno20KMkkcDZwTlX9xSL1BwJn\nV9WhSU4EqKqT+7pzgJP6RU+qqqf05Tsst4w1+QJPPv+UkWz3xI0vHcl2JUmStEuyVEXzI/RJArwT\n+NJgmE+y/8BizwAu7V9vAY5McpskBwEHA58FLgQOTnJQkg10F85uWY3PIEmSJN1ae8Ic+l8Engtc\nkuSivuwPgKOSHEY3gv514IUAVXVZkvfQXew6A7y4qmYBkhwPnAOMA6dW1WWr+UEkSZKkW6r5QF9V\n/87if4L44DLrvA543SLlH1xuPUmSJGm9aX7KjSRJkrQ3M9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BL\nkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuS\nJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5Ik\nSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJ\nDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkN\nM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9BLkiRJDTPQS5IkSQ0z0EuSJEkNM9AvkOTwJFck2ZbkhLVu\njyRJkrQcA/2AJOPAm4GnAocARyU5ZG1bJUmSJC3NQL+jRwHbquqqqpoCzgKOWOM2SZIkSUuaWOsG\nrDMHAN8ceL8dePRyK0xNTe1UNj4+zvj4OFXF9PT0SOpHZWpqiomJCcbGxjj5/FNGso8THvsSkoxs\n+ydufCkAMzMzzM3N7VCXhMnJyd1SPz09TVXtUD82NsbExMSq1K9V3xsfH2dubo6ZmZmd6uf7zqjr\n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\n",
            "text/plain": [
              "<Figure size 864x576 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab_type": "code",
        "outputId": "1428c733-d468-4cb8-84c7-f9153c6d15d4",
        "id": "rasz-WAS8baj",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 419
        }
      },
      "source": [
        "grouped_df_count = train_df.groupby(\"fullVisitorId\")[\"totals.transactionRevenue\"].count().reset_index()\n",
        "grouped_df_count.sort_values(by=['totals.transactionRevenue'], inplace=True, ascending=False)\n",
        "grouped_df_count"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>fullVisitorId</th>\n",
              "      <th>totals.transactionRevenue</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>7422</th>\n",
              "      <td>4064008221273566105</td>\n",
              "      <td>2</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5615</th>\n",
              "      <td>3102343581929921848</td>\n",
              "      <td>2</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18129</th>\n",
              "      <td>987390821892515431</td>\n",
              "      <td>2</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>830</th>\n",
              "      <td>0463325773564352787</td>\n",
              "      <td>2</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13763</th>\n",
              "      <td>747690048733385763</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6163</th>\n",
              "      <td>3396397804735366613</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6164</th>\n",
              "      <td>3396461882036302761</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6165</th>\n",
              "      <td>3396775680310832137</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6166</th>\n",
              "      <td>3398101758099870675</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18383</th>\n",
              "      <td>9999250019952621738</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>18384 rows × 2 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "             fullVisitorId  totals.transactionRevenue\n",
              "7422   4064008221273566105                          2\n",
              "5615   3102343581929921848                          2\n",
              "18129   987390821892515431                          2\n",
              "830    0463325773564352787                          2\n",
              "13763   747690048733385763                          1\n",
              "...                    ...                        ...\n",
              "6163   3396397804735366613                          0\n",
              "6164   3396461882036302761                          0\n",
              "6165   3396775680310832137                          0\n",
              "6166   3398101758099870675                          0\n",
              "18383  9999250019952621738                          0\n",
              "\n",
              "[18384 rows x 2 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 75
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab_type": "code",
        "outputId": "f221eb2a-6486-4c3e-b5a0-8784afe7cf14",
        "id": "187w0umb8EsZ",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 516
        }
      },
      "source": [
        "ax = grouped_df_count.hist('totals.transactionRevenue', bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)\n",
        "ax = ax[0]\n",
        "for x in ax:\n",
        "\n",
        "    # Despine\n",
        "    x.spines['right'].set_visible(False)\n",
        "    x.spines['top'].set_visible(False)\n",
        "    x.spines['left'].set_visible(False)\n",
        "\n",
        "    # Switch off ticks\n",
        "    x.tick_params(axis=\"both\", which=\"both\", bottom=\"off\", top=\"off\", labelbottom=\"on\", left=\"off\", right=\"off\", labelleft=\"on\")\n",
        "\n",
        "    # Draw horizontal axis lines\n",
        "    vals = x.get_yticks()\n",
        "    for tick in vals:\n",
        "        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)\n",
        "\n",
        "    # Remove title\n",
        "    x.set_title(\"\")\n",
        "\n",
        "    # Set x-axis label\n",
        "    x.set_xlabel(\"Total Transaction Count (per User)\", labelpad=20, weight='bold', size=12)\n",
        "\n",
        "    # Set y-axis label\n",
        "    x.set_ylabel(\"Visitors\", labelpad=20, weight='bold', size=14)\n",
        "\n"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAAvQAAAHzCAYAAABPMYkzAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0\ndHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nO3de5xdVX3//9dnzszgBVEQRQSVqPGC\nVBH5AdW2RkSIfL8KWquhrcRLjVoRfVS/lfj1q/y0FvxWa0svio1UqBWkWkqKIKZo6hUkKnJHIoKE\nRlBA0KLM7fP9Y6+BnclczpCcmVmZ1/Px2I9zzlp777POmpXJe++z9p7ITCRJkiTVqW++GyBJkiTp\ngTPQS5IkSRUz0EuSJEkVM9BXKCJWzXcbamJ/zZ59Njv21+zZZ7Njf82O/TV79tnsLLT+MtDXaUEN\nogrYX7Nnn82O/TV79tns2F+zY3/Nnn02Owuqvwz0kiRJUsX657sBO4A5v+/nqaeeOi/vWyv7a/bs\ns9mxv2bPPpsd+2t27K/Zs89mZ576K6as8D7028wOlCRJUq9NGeidciNJkiRVzEAvSZIkVcxAL0mS\nJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIk\nVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFWsmkAfEY+LiK9ExNURcVVEvK2U7xYR6yLi+vK4\naymPiDglIjZGxOURcUBrXyvL+tdHxMpW+XMi4oqyzSkREXP/SSVJkqTuVRPogRHgHZm5L3AI8JaI\n2Bc4AbgoM5cCF5XXAC8GlpZlFfAxaA4AgPcBBwMHAe8bPwgo67yhtd3yOfhckiRJ0gNWTaDPzM2Z\n+d3y/BfANcBewFHA6WW104Gjy/OjgDOycTHwiIjYEzgCWJeZd2TmncA6YHmp2yUzL87MBM5o7UuS\nJElakPrnuwEPRETsAzwbuATYIzM3l6qfAHuU53sBN7c221TKpivfNEn5tIaGhrYq63Q6dDodMpPh\n4eGe1Y+NjTEyMrJVfX9/P319fT2vHx0dZXR0dKv6gYEBIqJn9YODgwCMjIwwNja2RV1EMDAwMCf1\nw8PDNMd+9+vr66O/v39O6h17jr02x55jby7qHXuOvTbH3tyOvfGfxWSqOUM/LiJ2Bj4PvD0z727X\nlTPrOemG27cNqyJiQ0RsWLNmTa/fTpIkSYtcO3+WZdV9dROPRhayiBgAzgMuzMy/LGXXAcsyc3OZ\nNrM+M58aEaeW52e21xtfMvONpfxUYH1ZvpKZTyvlx7TXm0Y9HShJkqRaTXmzlmrO0Jc7znwSuGY8\nzBdrgfE71awEzm2VH1vudnMIcFeZmnMhcHhE7Fouhj2c5gBhM3B3RBxS3uvY1r4kSZKkBamaM/QR\n8VvA14ArgPFJVu+mmUd/NvB44CbglZl5Rwnlf0tzp5p7gNdm5oayr9eVbQE+mJn/WMoPBD4FPBi4\nAHhrztxBdXSgJEmSajblGfpqAv0CZgdKkiSp1+qfciNJkiRpawZ6SZIkqWIGekmSJKliBnpJkiSp\nYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKli\nBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIG\nekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6\nSZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWL9890APTAnrT+lJ/tdvez4nuxXkiRJveEZekmSJKli\nBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIGekmSJKliBnpJkiSpYgZ6SZIkqWIG\nekmSJKli1QT6iDgtIm6LiCtbZZ+NiMvKcmNEXFbK94mIX7XqPt7a5jkRcUVEbIyIUyIiSvluEbEu\nIq4vj7vO/aeUJEmSZqeaQA98CljeLsjMV2Xm/pm5P/B54F9b1T8cr8vMN7XKPwa8AVhalvF9ngBc\nlJlLgYvKa0mSJGlB65/vBnQrM78aEftMVlfOsr8SOHS6fUTEnsAumXlxeX0GcDRwAXAUsKysejqw\nHnjXTO0aGhraqqzT6dDpdMhMhoeHe1LfK0NDQ/T399PX18fY2BgjIyNbrTNePzo6yujo6Fb1AwMD\nRETP6gcHBwEYGRlhbGxsi7qIYGBgYE7qh4eHycwt6vv6+ujv75+T+vkae51OZ8ax0et6x55jbyLH\nnmPPsefY29HH3vjPYjI1naGfzm8Dt2bm9a2yJRHxvYj4z4j47VK2F7Cptc6mUgawR2ZuLs9/Auwx\n1ZtFxKqI2BARG9asWbOdPoIkSZI0uXb+LMuq++omHo0sZOUM/XmZud+E8o8BGzPzI+X1TsDOmXl7\nRDwH+DfgGcBTgJMz87Cy3m8D78rM/xkRP8/MR7T2eWdmdjOPfl468KT1p/Rkv6uXHd+T/UqSJGmb\nxFQV1Uy5mUpE9AMvB54zXpaZ9wL3luffiYgf0oT5W4C9W5vvXcoAbo2IPTNzc5mac9tctF+SJEna\nFjvClJvDgGsz876pNBHxqIjolOdPpLn49YYypebuiDikzLs/Fji3bLYWWFmer2yVS5IkSQtWNYE+\nIs4EvgU8NSI2RcTrS9UK4MwJq/8OcHm5jeXngDdl5h2l7o+BNcBG4Ic0F8QCnAy8KCKupzlIOLln\nH0aSJEnaTqqZcpOZx0xR/ppJyj5PcxvLydbfAOw3SfntwAu3rZWSJEnS3KrmDL0kSZKkrRnoJUmS\npIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKk\nihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSK\nGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ\n6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihno\nJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKVRPo\nI+K0iLgtIq5slZ0YEbdExGVlObJVtzoiNkbEdRFxRKt8eSnbGBEntMqXRMQlpfyzETE4d59OkiRJ\nemCqCfTAp4Dlk5R/NDP3L8v5ABGxL7ACeEbZ5u8johMRHeDvgBcD+wLHlHUBPlT29WTgTuD1Pf00\nkiRJ0nZQTaDPzK8Cd3S5+lHAWZl5b2b+CNgIHFSWjZl5Q2YOAWcBR0VEAIcCnyvbnw4cvV0/gCRJ\nktQD/fPdgO3guIg4FtgAvCMz7wT2Ai5urbOplAHcPKH8YOCRwM8zc2SS9ac1NDS0VVmn06HT6ZCZ\nDA8P96S+V4aGhujv76evr4+xsTFGRka2Wme8fnR0lNHR0a3qBwYGiIie1Q8ONrOhRkZGGBsb26Iu\nIhgYGJiT+uHhYTJzi/q+vj76+/vnpH6+xl6n05lxbPS63rHn2JvIsefYc+w59nb0sTf+s5hMNWfo\np/Ax4EnA/sBm4CNz8aYRsSoiNkTEhjVr1szFW0qSJGkRa+fPsqy6r27i0chCFhH7AOdl5n7T1UXE\naoDMPKnUXQicWFY9MTOPKOWrS9nJwE+Bx2TmSET8Znu9GcxLB560/pSe7Hf1suN7sl9JkiRtk5iq\nouoz9BGxZ+vly4DxO+CsBVZExE4RsQRYCnwbuBRYWu5oM0hz4ezabI5qvgK8omy/Ejh3Lj6DJEmS\ntC2qmUMfEWcCy4DdI2IT8D5gWUTsT3OW/EbgjQCZeVVEnA1cDYwAb8nM0bKf44ALgQ5wWmZeVd7i\nXcBZEfFnwPeAT87RR5MkSZIesKqm3CxQTrmRJElSr+2YU24kSZKkxc5AL0mSJFXMQC9JkiRVzEAv\nSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9J\nkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mS\nJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIk\nVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRV\nzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVayaQB8Rp0XE\nbRFxZavsLyLi2oi4PCLOiYhHlPJ9IuJXEXFZWT7e2uY5EXFFRGyMiFMiIkr5bhGxLiKuL4+7zv2n\nlCRJkmanmkAPfApYPqFsHbBfZj4T+AGwulX3w8zcvyxvapV/DHgDsLQs4/s8AbgoM5cCF5XXkiRJ\n0oJWTaDPzK8Cd0wo+1JmjpSXFwN7T7ePiNgT2CUzL87MBM4Aji7VRwGnl+ent8olSZKkBat/vhuw\nHb0O+Gzr9ZKI+B5wN/CezPwasBewqbXOplIGsEdmbi7PfwLs0c2bDg0NbVXW6XTodDpkJsPDwz2p\n75WhoSH6+/vp6+tjbGyMkZGRrdYZrx8dHWV0dHSr+oGBASKiZ/WDg4MAjIyMMDY2tkVdRDAwMDAn\n9cPDwzTHhffr6+ujv79/Turna+x1Op0Zx0av6x17jr2JHHuOPceeY29HH3vjP4vJVHOGfjoR8b+B\nEeCfS9Fm4PGZ+WzgT4DPRMQu3e6vnL3PqeojYlVEbIiIDWvWrNmGlkuSJEkza+fPsqy6r27i0chC\nFhH7AOdl5n6tstcAbwRemJn3TLHdeuCdwC3AVzLzaaX8GGBZZr4xIq4rzzeXqTnrM/OpXTRrXjrw\npPWn9GS/q5cd35P9SpIkaZvEVBVVn6GPiOXAnwIvbYf5iHhURHTK8yfSXPx6Q5lSc3dEHFLubnMs\ncG7ZbC2wsjxf2SqXJEmSFqxq5tBHxJnAMmD3iNgEvI/mrjY7AevK3ScvLne0+R3g/RExDIwBb8rM\n8Qtq/5jmjjkPBi4oC8DJwNkR8XrgJuCVc/CxJEmSpG1STaDPzGMmKf7kFOt+Hvj8FHUbgP0mKb8d\neOG2tFGSJEmaa1VPuZEkSZIWOwO9JEmSVDEDvSRJklQxA70kSZJUMQO9JEmSVDEDvSRJklQxA70k\nSZJUMQO9JEmSVDEDvSRJklSxrgJ9RDwsIh4bEQ8qr4+KiL+OiNf1tnmSJEmSptPf5XqfAF4JHBIR\njwTOARIgInbLzA/3qH2SJEmSptHtlJsDgLsz81LgFaXsOiCAlb1omCRJkqSZdRvo9wJuKs+fCVyd\nmfsCPwKe0IuGSZIkSZpZt4F+FHhweb4UuKI8v5vmLL0kSZKkedBtoN8IPDkirgV2Ab5Tyh8L3NKL\nhkmSJEmaWbeB/qPl8SnAncA/RcRvAI8CLu1FwyRJkiTNrKu73GTmpyPi+zTTbb6RmbdGRB/wIuCG\nXjZQkiRJ0tRmDPQRMQBcDPwCeEFmJkBmbgY297Z5kiRJkqYz45SbzBwGHg/sOh7mJUmSJC0M3c6h\nPx14SkQ8o5eNkSRJkjQ73f6l2EfT3J5yQ0R8BbiV8pdigczM1/eicZIkSZKm122g/0OaAB/AEa3y\nKOUGekmSJGkedBvof8z9Z+QlSZIkLRDd3rZynx63Q5IkSdID0O0ZegDKRbEHlpcbMvOq7d8kSZIk\nSd3qKtBHRD9wBvCqCeVnAiszc7QHbZMkSZI0g25vW/mnwAqai2DbyzGlTpIkSdI86DbQH0tzUeyH\ngGeV5f/ShPpje9M0SZIkSTPpdg79PsAPMnN1q+yEiDgaWLLdWyVJkiSpK92eof818OiI2GW8ICIe\nTvMHp37Vi4ZJkiRJmlm3Z+gvAQ4DLo+IL5ay5cDDgS/1omGSJEmSZtZtoP8A8ALg8cAbSlkAw6VO\nkiRJ0jzoaspNZn4dOBz4Gs30m18DXwUOz8xv9q55kiRJkqbT9R+Wysz1wPN71xRJkiRJs9XVGfqI\nGI2Ib0xSflpEXLL9myVJkiSpG92eoR//Q1ITPRN49vZrjiRJkqTZmDbQR8RprZdPmvD6ocD+NPPp\nJUmSJM2Dmc7Qv4bmL8QC7A6snFAfwGXbuU2SJEmSujRToP8xTaB/PDAE/KRVdw9wLfCe3jRNkiRJ\n0kymDfSZuQ9ARIwB38vM585FoyRJkiR1p9uLYpcA9/ayIZIkSZJmb8pAXy6A3ZiZfw68r5RNtmpm\n5ut70zxJkiRJ05nuDP1rgG8Bf86WF8e2RSk30EuSJEnzYLo/LPVj7r8I9sdTLDeVxzlR/pDVbRFx\nZatst4hYFxHXl8ddS3lExCkRsTEiLo+IA1rbrCzrXx8RK1vlz4mIK8o2p8QUX0lIkiRJC8WUgT4z\n98nM3209XzLVMnfN5VPA8gllJwAXZeZS4KLyGuDFwNKyrAI+Bs0BAM0UooOBg4D3jR8ElHXe0Npu\n4ntJkiRJC8p0Z+inFBF7RcTLIuIp27tB08nMrwJ3TCg+Cji9PD8dOLpVfkY2LgYeERF7AkcA6zLz\njsy8E1gHLC91u2TmxZmZwBmtfUmSJEkLUld3uYmIk4DfBY4FfgF8E9gZGI2Il2fmeb1r4oz2yMzN\n5flPgD3K872Am1vrbSpl05VvmqR8WkNDQ1uVdTodOp0Omcnw8HBP6ntlaGiI/v5++vr6GBsbY2Rk\nZKt1xutHR0cZHR3dqn5gYICI6Fn94OAgACMjI4yNjW1RFxEMDAzMSf3w8DDNsd/9+vr66O/vn5P6\n+Rp7nU5nxrHR63rHnmNvIseeY8+x59jb0cfe+M9iMt2eoV8O7A18D3gd8DCaC2L7gXd1uY+eK2fW\nJ7t4d7uKiFURsSEiNqxZs6bXbydJkqRFrp0/y7LqvrqJRyNT7OAO4NbMfHpErAeeBBwIXAF0MvOR\nPWr7ZG3ZBzgvM/crr68DlmXm5jJtZn1mPjUiTi3Pz2yvN75k5htL+anA+rJ8JTOfVsqPaa83jZ4f\nQEzmpPWn9GS/q5cd35P9SpIkaZtMebOWbs/QPwj4VXn+FJq/GnsrzR1uHrJtbdtma4HxO9WsBM5t\nlR9b7nZzCHBXmZpzIXB4ROxaLoY9HLiw1N0dEYeUu9sc29qXJEmStCB1+5dibwH2i4h/oJmj/v1S\n/ijgtl40bDIRcSbNGfbdI2ITzd1qTgbOjojX09xG85Vl9fOBI4GNwD3AawEy846I+ABwaVnv/Zk5\nfqHtH9PcSefBwAVlkSRJkhasbgP9Z4F30/wBqTHgXyLisTTz6r/Qo7ZtJTOPmaLqhZOsm8BbptjP\nacBpk5RvAPbbljZKkiRJc6nbQP9e4Faae7Ofl5mXR8Rv0PwV2f/sVeMkSZIkTa+rQJ+ZY8DfTCi7\nguaiWEmSJEnzZMpAHxHvBTZl5mnl+ZQy8/3bvWWSJEmSZjTdGfoTgW/RzDU/kelvz2iglyRJkubB\nTFNuYornkiRJkhaAKe9Dn5l9wIaIeFZm9k23zGF7JUmSJLXMFMaPA74bEd+NiLdGxJz9RVhJkiRJ\nM5sp0I/QTLXZH/gr4JaI+HxE/M+I8My8JEmSNM9mCuV7Am8DNtAE+0HgaOBcYFNEfCgi9u1tEyVJ\nkiRNZdpAn5m3Z+bfZOZBwL7Ah4BNNOH+McA7gct73kpJkiRJk+p62kxmXpuZqzPzCcCxwC9ogr13\nv5EkSZLmSVd/KRYgIh4M/C7wauBQZnEwIEmSJKk3Zgz0EXEozRn5lwMPHS8GxoB1wD/2rHWSJEmS\npjVtoI+IHwN7jb8sjxuBTwFnZOam3jVNkiRJ0kxmOkO/d3n8JXA28I+Z+Y3eNkmSJElSt2YK9P9J\nM6Xmc5l5zxy0R5IkSdIsTBvoM/MFc9UQSZIkSbPnnWokSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKk\nihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSK\nGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIoZ\n6CVJkqSKGeglSZKkihnoJUmSpIoZ6CVJkqSKGeglSZKkihnoJUmSpIpVH+gj4qkRcVlruTsi3h4R\nJ0bELa3yI1vbrI6IjRFxXUQc0SpfXso2RsQJ8/OJJEmSpO71z3cDtlVmXgfsDxARHeAW4BzgtcBH\nM/PD7fUjYl9gBfAM4LHAf0TEU0r13wEvAjYBl0bE2sy8ek4+iCRJkvQAVB/oJ3gh8MPMvCkiplrn\nKOCszLwX+FFEbAQOKnUbM/MGgIg4q6w7baAfGhraqqzT6dDpdMhMhoeHe1LfK0NDQ/T399PX18fY\n2BgjIyNbrTNePzo6yujo6Fb1AwMDRETP6gcHBwEYGRlhbGxsi7qIYGBgYE7qh4eHycwt6vv6+ujv\n75+T+vkae51OZ8ax0et6x55jbyLHnmPPsefY29HH3vjPYjLVT7mZYAVwZuv1cRFxeUScFhG7lrK9\ngJtb62wqZVOVbyUiVkXEhojYsGbNmu3XekmSJGkS7fxZllX31U08GqlVRAwC/wU8IzNvjYg9gJ8B\nCXwA2DMzXxcRfwtcnJmfLtt9Erig7GZ5Zv5RKX81cHBmHjfDW89LB560/pSe7Hf1suN7sl9JkiRt\nkymnn+xIU25eDHw3M28FGH8EiIh/AM4rL28BHtfabu9SxjTlkiRJ0oK0I025OYbWdJuI2LNV9zLg\nyvJ8LbAiInaKiCXAUuDbwKXA0ohYUs72ryjrSpIkSQvWDnGGPiIeSnN3mje2iv9vROxPMyXmxvG6\nzLwqIs6mudh1BHhLZo6W/RwHXAh0gNMy86o5+xCSJEnSA7BDBPrM/G/gkRPKXj3N+h8EPjhJ+fnA\n+du9gZIkSVKP7EhTbiRJkqRFx0AvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9J\nkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mS\nJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIk\nVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRV\nzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVzEAvSZIkVcxAL0mSJFXM\nQC9JkiRVzEAvSZIkVcxAL0mSJFXMQC9JkiRVbIcJ9BFxY0RcERGXRcSGUrZbRKyLiOvL466lPCLi\nlIjYGBGXR8QBrf2sLOtfHxEr5+vzSJIkSd3YYQJ98YLM3D8zDyyvTwAuysylwEXlNcCLgaVlWQV8\nDJoDAOB9wMHAQcD7xg8CJEmSpIWof74b0GNHAcvK89OB9cC7SvkZmZnAxRHxiIjYs6y7LjPvAIiI\ndcBy4Myp3mBoaGirsk6nQ6fTITMZHh7uSX2vDA0N0d/fT19fH2NjY4yMjGy1znj96Ogoo6OjW9UP\nDAwQET2rHxwcBGBkZISxsbEt6iKCgYGBOakfHh6mGUL36+vro7+/f07q52vsdTqdGcdGr+sde469\niRx7jj3HnmNvRx974z+LyexIZ+gT+FJEfCciVpWyPTJzc3n+E2CP8nwv4ObWtptK2VTlW4iIVRGx\nISI2rFmzZnt+BkmSJGkr7fxZllX31U08GqlVROyVmbdExKOBdcBbgbWZ+YjWOndm5q4RcR5wcmZ+\nvZRfRHPmfhnwoMz8s1L+f4BfZeaHp3nreenAk9af0pP9rl52fE/2K0mSpG0SU1XsMGfoM/OW8ngb\ncA7NHPhby1QayuNtZfVbgMe1Nt+7lE1VLkmSJC1IO0Sgj4iHRsTDxp8DhwNXAmuB8TvVrATOLc/X\nAseWu90cAtxVpuZcCBweEbuWi2EPL2WSJEnSgrSjXBS7B3BOREDzmT6TmV+MiEuBsyPi9cBNwCvL\n+ucDRwIbgXuA1wJk5h0R8QHg0rLe+8cvkJUkSZIWoh0i0GfmDcCzJim/HXjhJOUJvGWKfZ0GnLa9\n2yhJkiT1wg4x5UaSJElarAz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElS\nxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLF\nDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM\n9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0\nkiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSS\nJElSxQz0kiRJUsUM9JIkSVLFqg/0EfG4iPhKRFwdEVdFxNtK+YkRcUtEXFaWI1vbrI6IjRFxXUQc\n0SpfXso2RsQJ8/F5JEmSpNnon+8GbAcjwDsy87sR8TDgOxGxrtR9NDM/3F45IvYFVgDPAB4L/EdE\nPKVU/x3wImATcGlErM3Mq+fkU0iSJEkPQPWBPjM3A5vL819ExDXAXtNschRwVmbeC/woIjYCB5W6\njZl5A0BEnFXWNdBLkiRpwao+0LdFxD7As4FLgOcBx0XEscAGmrP4d9KE/Ytbm23i/gOAmyeUHzzT\new4NDW1V1ul06HQ6ZCbDw8M9qe+VoaEh+vv76evrY2xsjJGRka3WGa8fHR1ldHR0q/qBgQEiomf1\ng4ODAIyMjDA2NrZFXUQwMNgijyIAABPWSURBVDAwJ/XDw8Nk5hb1fX199Pf3z0n9fI29Tqcz49jo\ndb1jz7E3kWPPsefYc+zt6GNv/Gcxmern0I+LiJ2BzwNvz8y7gY8BTwL2pzmD/5Ht+F6rImJDRGxY\ns2bN9tqtJEmSNKl2/izLqvvqJh6N1CgiBoDzgAsz8y8nqd8HOC8z94uI1QCZeVKpuxA4sax6YmYe\nUcq3WG8a89KBJ60/pSf7Xb3s+J7sV5IkSdskpqqo/gx9RATwSeCadpiPiD1bq70MuLI8XwusiIid\nImIJsBT4NnApsDQilkTEIM2Fs2vn4jNIkiRJD9SOMIf+ecCrgSsi4rJS9m7gmIjYn+YM+o3AGwEy\n86qIOJvmYtcR4C2ZOQoQEccBFwId4LTMvGouP4gkSZI0W9UH+sz8OpN/BXH+NNt8EPjgJOXnT7ed\nJEmStNBUP+VGkiRJWswM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM\n9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0\nkiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSS\nJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIk\nSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJUsUM9JIkSVLFDPSSJElSxQz0kiRJ\nUsUM9JIkSVLFDPSSJElSxQz0kiRJUsX657sBC01ELAf+GugAazLz5HlukiRV4aT1p/Rkv6uXHd+T\n/UrSjsIz9C0R0QH+DngxsC9wTETsO7+tkiRJkqZmoN/SQcDGzLwhM4eAs4Cj5rlNkiRJ0pSccrOl\nvYCbW683AQdPt8HQ0NBWZZ1Oh06nQ2YyPDzck/peGRoaor+/n76+PsbGxhgZGdlqnfH60dFRRkdH\n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\n",
            "text/plain": [
              "<Figure size 864x576 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kqWDhqmgPbMh",
        "colab_type": "text"
      },
      "source": [
        "## **numpy.log1p() in Python**\n",
        "**numpy.log1p(arr, out = None, *, where = True, casting = ‘same_kind’, order = ‘K’, dtype = None, ufunc ‘log1p’) :**\n",
        "\n",
        "This mathematical function helps user to calculate **natural logarithmic value of x+1** where x belongs to all the input array elements.\n",
        "\n",
        "* **log1p is reverse of exp(x) – 1.**\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "xsf9oYbUJAaq",
        "colab_type": "code",
        "outputId": "e12fd0ef-835a-49d3-ce06-e82074b035a6",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 685
        }
      },
      "source": [
        "plt.figure(figsize=(15,10))\n",
        "plt.scatter(range(grouped_df_sum.shape[0]), np.sort(np.log1p(grouped_df_sum[\"totals.transactionRevenue\"].values)))\n",
        "plt.title('Total Transaction Revenue for each Visitor')\n",
        "plt.xlabel('index', fontsize=14)\n",
        "plt.ylabel('TransactionRevenue', fontsize=14)\n",
        "plt.show()"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAA3kAAAJgCAYAAAA3XqoyAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0\ndHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nOzde7xldV0//tfbYbDBGyADAoKoGYla\noqSW5te8oV0Eo7xkiuUlS0u/JqXp10uZZeStzPyRmpgG3gC1KDTzkt9SBEGGiyPqF9ThNigjpKPA\n8Pn9sdfBzemcmX3O2fvsc9Z5Ph+P/Thrf9Zee7/3+ux95rzms9ZnVWstAAAA9MOtpl0AAAAA4yPk\nAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAewwlXVj1RVq6o7T7uW5VBV96yqq6ddx2pV\nVW+oqm9X1VenXct8quoDVfXiMT7fJVX1U7t4jM8VsGYIeQCLUFX/PXS7qaq2D91/yi62fUxVfWVM\ndXx16HV3VNX3h+6/cByvMWlVdXVVPWjmfmvtotbaPhN4ndt2Yfm73f75RlW9pqpq3K81LVV1zyTP\nSHL31trdp13PUlXV7avqe1X1gDnW/V1VvTNJWmuHtNY+v7Pnmv25qqqzqupJYy8aYAXYbdoFAKxG\nrbXbzixX1SVJntla+7cp1HHzH/JV9dkkb26tvXu+x1fVbq21G5eluJXr7q21K7pA9B9JNiU5aco1\njctdklzWWrtmoRuuxM9Ga+3aqjo1ydOSnDnTXlU/kuRXkzx+GnVV1a0G5bU2jdcH2BUjeQATUFUb\nqupvquryqvpmVR1fVeur6o5JTk1yt6ERtztW1YOr6nNVta2qLusOuVvyf8RV1fOq6mNV9daquibJ\ni6rqsKr6dHdI31VV9fdVNRxar66q51fVhVX1nap6V1Wt79YdUFVndHV+q6o+OrTdq7rD5q6rqk1V\n9dihdVVVv1tVm7v153V1nJrkjkn+vdsXv1NV966q7w9te5eq+pequqbb/teH1v1lV997u+f9YlXd\nZ5R901q7KIPgcN+h57tjVb27qq6oqq9X1cu62m/XjQDedeixB3ejTLfv7h/Tve9tVfWpqvrxEffp\n86rqX4ceOzPieKfu/h5V9dfd5+jyqnpTVe0+R18fncFn68e6ffnmrv0JVXVRt/8+VlXD/zFwdVW9\nsKouTPLtufZTVf1EVX2y2/7CqvqloXXHdH15XVVdWlV/OGvbR1TVmd17vrSqnji0et+unuuq6jNV\nddA8XXVikifN7K/O45J8J8knh97Hg7rln62qc6vq2m5/vbprv/lzVVVvTHJ4knd2++q1XfvPVdU5\nXb3/VVX3H3ovZ1XVK6vqzCTfS7LfPPUCTJ2QBzAZr0ryE0nuk+T+SR6W5A9aa9/KYPTha62123a3\nbyW5IcnzMgg8P5vkl5I8c0y1/FySzyXZJ8mburaXZ/BH6k8muVeS2edHHZPkfyW5R1fPzB/nL0ly\nfvdc+yd59dA2FyV5UJI9k7w+yclVtXe37ulJ/neSJyS5fffzO621xyf5VpKHd/viLcNFVFUl+WCS\nC5LcKclTk/x1VT1wVq3/X/e6n07yhlF2ShcGH5hk+NDZk5NsTXLX7r08IcmvtdauS/LPSYYP73ty\nktO70aaHJPnrJMdm0IfvTXJqVa2bVedc+3RX3pRk3wz66Z7dz+NmP6i1dloGo1tf7vbl86rqvkne\nnuS3Mujv/0xy2qy6npDkEZkjtFTVnkk+muStGfT5byY5cSjsXtu9jzt07+/FVfXIbttDk3woyZ91\n++SnMviMzPi17n3cMYN9/op53v+/Jfl+kl8Yantqkn+YZyTtLUle1Vq7fZJDk3x49gNaay9Ick6S\np3f76g+rav/usa/uanp7ktOr6nZDm/56kqdk8BneOk+9AFMn5AFMxlOSvKK1dnVr7coM/nB86nwP\nbq2d2Vr7fGttR2vtq0nelkEgGIcvt9b+vnvu7a21C1trn2yt3dBauzzJX83xWq9vrW1trV2V5F/y\nw9GuG5IcmOSg1tr1rbVPD72Hk1trV3Sv8/cZ/BF8eLf6mUn+tLX2xTbwpdbalhFq//EkhyV5WWvt\nB621M5O8O7fclx9rrf17a21Hkn8YqnU+m6vqe0nOS3Jakr9Pkm6E64FJjuv202UZBLeZYPePGQS7\nGb/WtSWDEPWm1toXuvf/lgyCwHAt8+3TeXUjdk9P8nutte+01rYleW1uGTZ35slJ3t9a+3Rr7fok\nf5JB/x0+9JjXt9Yub61tn2P7Y5Kc0/XtjtbaZ7vafzlJWmsf6851u6m1dlYGgXzms/S0JKe21k5t\nrd3YWruqtXbe0HOf3Fo7t6vrpPn2R2vtpgz6/GndPtmY5Mgk75rnPd+QwWjm3q21a7vPzCiOTvL5\n1toHu3rfluSq7rVmnNBau7j77O8Y8XkBlp2QBzBm3ejTnZJcOtR8aQZ/XM+3zWHdIYlXVtW1GYy0\njWvykW/Meq0712B2w8u615oZpRl2xdDy95LMHM75JxmEt09V1Zer6gVDz/vsocMVtyU5ZOh5D0qy\nmNkeD0hyZWvt+0Nts/flfLXO59DuMb+R5CFJNnTtd0lymyRXD72H1+WHI1ynJzmoqu5VVYd1j//n\noW1fPrNdt+1eS6wzSe6cwfnzm4ee9wMZjOyN4oAMfQ67c+4um1XXN2ZvNOQuSR4+630dlcEobqrq\noTU49PfqqvpOBiNdo/b5QvbHiUl+oRsZfnKSs1trX57nsU9NckSSi6vqs1X1qJ0877Bb7KvO7M/a\nzvYVwIoh5AGMWXcI2RUZ/IE84+AkMyNXcx1i9ndJvpDBpCC3T/LHScY16+Ps13tdBuczHda91nNG\nfa3W2jWttd9trR2cwWF6r6yqB3ah5/UZzOy4d2ttzySXDD3vN5LMN9vjziavuCzJflV166G24X25\nKN3I0zuTfCnJzHlk38hgv+zVWtuzu92+tfaAbpvrk5ySQch4SpIPttZ+MLTtHw1tt2drbY/W2v84\nVHAO302yx9D9Ow0tX5ZkR5JDhp73Dq21Uc8HuyxDn8ManOd5QG65/3a2/7+RwSGpw+/rtq21F3Xr\n35/BKNuBrbU7dMuj9PmCdOdPfjGDEcynZhD65nvsBa21X80gCP9tklNq7vNbZ7/vW+yrzuzPmolW\ngFVByAOYjJOSvKIGE3nsm+SlGfwBnCRXZjDpxPDIxe0yOEftv6vqXkmeNcHabpfkuiTXVtUhGZwr\nN5KqOqqq7tqNVn4nyU3d7bbdz61JblVVz8tgJG/G25L8UTeJR1XVj1fVzAjJlUnuNs9Lfqm7/UlV\n7V5VR2QwWvSeUWvehT9L8rtVtVdr7eIMztN6TQ0mP7lVVf1YVT146PEzh2w+KT88VDMZnBP4gqq6\nX/f+bldVR9dgFshdOTfJEd0+2SODUdwkSTeCeWKSN3WfparBhC+PHPH9nZzkV2owsc/6DD6Hl3fv\ncxSnJHlAVf1KVe3W9cFPV9WP1mCGydtkcE7l9d15iccMbfuuJEdX1eOqal1V7VsjToozjxOT/EEG\n57m+d74HVdXTukM1d+SHn9G5wtnsz92Huvd6dPdefyODwP3RObYFWNGEPIDJeHmSCzOYMOTcJP83\nyV90676YwQQPl3aHwO2dQdB6ZlX9d5K/yU7+iB2Dl2UwGcu1GRz69/4FbHuvJJ/KICR+IslrunMJ\nz8xgoopzMhgROSCD9z3jnRmc3/bB7nXfm8E5a8ngfMW/qMHsjb89/GLdqOgxGUwQc2UGwep/t9b+\nawE1z6s7x+y8JDOHnT4hg8MzN2cw2+RJSTYObfKJDA7v3NAtzzzPpzPow7cl2dZt/8SMMPLTWjsn\ng8li/jODz8zHZz3kdzMIz2dnEFpOz/yheK7n/q0M+mZrkocmOXrU88naYFKgIzP4T4crMujbP06y\nvjtX7jkZTAzznSQvzODzNLPt5gwmGXp5kmsymMn0nqO87jxOyuAw0Y+0nV8i4qgkX66q6zKYAOmJ\n87zf1yV5Rvcd/LPuHMyjkrwyg+D6nCS/0Fq7dgk1A0xFNZd4AQAA6A0jeQAAAD0i5AEAAPSIkAcA\nANAjQh4AAECPzHXdmBVvn332aYcccsi0ywAAAJiKs88+++rW2sa51q3KkHfIIYfkrLPOmnYZAAAA\nU1FVl863zuGaAAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECP\nCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i\n5AEAAPSIkAcAANAjQh4AAECP7DbtAgAAAFaa087ZkuPP2JzLtm3PAXtuyHFHHpqjDz9w2mWNRMgD\nAAAYcto5W/KSUzZl+w07kiRbtm3PS07ZlCSrIug5XBMAAGDI8Wdsvjngzdh+w44cf8bmKVW0MEIe\nAADAkC3bti+ofaUR8gAAAIasq1pQ+0oj5AEAAAzZ0dqC2lcaIQ8AAGDIgXtuWFD7SiPkAQAADPm5\nH9+4oPaVRsgDAAAY8okvbV1Q+0oj5AEAAAy5bJ5ZNOdrX2mEPAAAgCEHzHPu3XztK42QBwAAMOS4\nIw/NhvXrbtG2Yf26HHfkoVOqaGF2m3YBAAAAK8nRhx+YJDn+jM25bNv2HLDnhhx35KE3t690Qh4A\nAMAsRx9+4KoJdbM5XBMAAKBHjOQBAADMcto5WxyuCQAA0AennbMlx33gi7lhR0uSbNm2Pcd94ItJ\nsiqCnsM1AQAAhrzqIxfcHPBm3LCj5VUfuWBKFS2MkAcAADDkmu/dsKD2lUbIAwAA6BEhDwAAoEeW\nLeRV1UFV9YmqurCqLqiq53fte1fVx6rq4u7nXstVEwAAQN8s50jejUl+v7V2WJIHJXluVR2W5MVJ\nPt5au0eSj3f3AQAAWIRlC3mttctba1/olq9LclGSA5McleTE7mEnJjl6uWoCAACYbf08KWm+9pVm\nKmVW1SFJDk/yuST7tdYu71ZdkWS/ebZ5dlWdVVVnbd26dVnqBAAA1p4bblpY+0qz7CGvqm6b5INJ\nXtBau3Z4XWutJWlzbddaO6G1dkRr7YiNGzcuQ6UAAACrz7KGvKpan0HAe09r7ZSu+cqq2r9bv3+S\nq5azJgAAgGG7r6s52/fcsH6ZK1mc5Zxds5K8PclFrbXXD636cJJju+Vjk3xouWoCAAAY9rLTNuX6\nHf/z4MJK8srH3Wv5C1qE3ZbxtR6c5KlJNlXVuV3bHyX58yTvq6pnJLk0yROWsSYAAICbnfS5b8y7\n7ujDD1zGShZv2UJea+0zGQTguTxiueoAAACYz4425xQhc08cskKtkklAAQAAJm++Uan52lciIQ8A\nAKAz34idkTwAAACmQsgDAADoESEPAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEeEPAAAgB4R\n8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAABIcto5W6ZdwlgIeQAAAEleeuqmaZcw\nFkIeAABAku9ev2PaJYyFkAcAALALB+65YdoljEzIAwAASFI7WXfckYcuWx1LJeQBAAAkecqDDp6z\n/cF33ztHH37gMlezeEIeAABAkiPusvec7b96xNzhb6US8gAAAJK86iMXLKh9pRLyAAAAklzzvRsW\n1L5SCXkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAA\nwJp32jlbpl3C2Ah5AADAmveHHzxv2iWMjZAHAACseT+48aZplzA2Qh4AAMBOrKuadgkLIuQBAADs\nxJMfeNC0S1gQIQ8AAGAnXn30faZdwoIIeQAAAD0i5AEAAPSIkAcAANAjQh4AAECPCHkAAAA9IuQB\nAABr2qNe/8lplzBWQh4AALCmXXzVd6ddwlgJeQAAAD0i5AEAAPSIkAcAADCPX3/QwdMuYcGEPAAA\ngHm8+uj7TLuEBRPyAAAAekTIAwAA6BEhDwAAWLNOO2fLtEsYOyEPAABYs/7wg+dNu4SxE/IAAIA1\n6wc33jTtEsZOyAMAAJjDg+++97RLWBQhDwAAYA7vedZPT7uERRHyAAAAekTIAwAA6BEhDwAAoEeE\nPAAAgB4R8gAAAHpEyAMAANakl522adolTISQBwAArEnv/uzXp13CRAh5AAAAPSLkAQAAzPLgu+89\n7RIWTcgDAACY5T3P+ulpl7BoQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AADAmnPa\nOVumXcLECHkAAMCac/wZm6ddwsQIeQAAwJqzZdv2aZcwMUIeAABAjwh5AAAAQ+6x722mXcKSCHkA\nAABDPvbCh027hCUR8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8\nAACAHhHyAAAAekTIAwAA6BEhDwAAoEeEPAAAYE057Zwt0y5hooQ8AABgTXnpqZumXcJECXkAAMCa\n8t3rd0y7hIkS8gAAADoH7rlh2iUsmZAHAADQOe7IQ6ddwpIJeQAAAJ2jDz9w2iUsmZAHAADQI0Ie\nAACwptQC21cbIQ8AAFhT2gLbVxshDwAAWFPmm0GzDzNrJkIeAACwxhx35KFZv+6WB2euX1e9mFkz\nEfIAAIC1aPaxmX05VjNCHgAAsMYcf8bm3HDTLVPdDTe1HH/G5ilVNF5CHgAAsKZctm37gtpXGyEP\nAABYUw6YZ4KV+dpXGyEPAABYU4478tBsWL/uFm0b1q/rzcQru027AAAAgOV09OEHJhmcm3fZtu05\nYM8NOe7IQ29uX+2M5AEAAPSIkTwAAGBNOe2cLXnJKZuy/YYdSZIt27bnJadsSpJejOYZyQMAANaU\n48/YfHPAm7H9hh0uoQAAALAauYTCmFTVO6rqqqo6f6jtlVW1parO7W4/v1z1AAAAa9Oee6xfUPtq\ns5wjee9M8pg52t/QWrtvdzt9GesBAADWoNYW1r7aLFvIa619Osm3l+v1AAAA5vKd7TcsqH21WQnn\n5D2vqs7rDufca74HVdWzq+qsqjpr69aty1kfAADQIwfsuWFB7avNtEPe3ya5e5L7Jrk8yevme2Br\n7YTW2hGttSM2bty4XPUBAAA9c9yRh2bD+nW3aNuwfl2OO/LQKVU0XlO9Tl5r7cqZ5ar6uyT/NMVy\nAACANWDmWnjHn7E5l23bngP23JDjjjy0F9fIS6Yc8qpq/9ba5d3dxyc5f2ePBwAAGIejDz+wN6Fu\ntmULeVV1UpKHJdmnqr6Z5BVJHlZV903SklyS5LeWqx4AAIA+WraQ11p78hzNb1+u1wcAAFgLpj3x\nCgAAAGMk5AEAAPSIkAcAANAjU51dEwAAYBpOO2eLSygAAAD0wWnnbMlLTtmU7TfsSJJs2bY9Lzll\nU5L0Iug5XBMAAFhTjj9j880Bb8b2G3bk+DM2T6mi8RLyAACANeWybdsX1L7aCHkAAMCacsCeGxbU\nvtoIeQAAwJpy3JGHZsP6dbdo27B+XY478tApVTReJl4BAADWlJnJVcyuCQAA0BNHH35gb0LdbA7X\nBAAA6BEhDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAADoESEP\nAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgRIQ8AAKBHhDwA\nAIAeEfIAAAB6RMgDAADokQWFvKq6d1UdVVV7dPd3q6qaTGkAAAAs1Eghr6r2qapPJjkvySlJ7tSt\nemuS10+mNAAAABZq1JG8NyT5XpIDup8z3pfkyHEXBQAAwOLsNuLjHpXk0a21K2YdnXlxkoPHXhUA\nAACLMupI3m1yyxG8GXdMcv34ygEAAGApRg15n0ny60P3WzfhyouSfHLcRQEAALA4ox6u+QdJPlVV\n90+ye5I/S3KvJPsn+ZkJ1QYAAMACjTSS11rblOQnklyY5D+S7JvkjCSHt9a+PLnyAAAAWIhRR/LS\nWvtmkj+cYC0AAAAs0Ughr6oO29n61tqF4ykHAACApRh1JO/8JC3J8PUT2tDyurFVBAAAwKKNGvLu\nOev++iSHZ3D45kvGWhEAAACLNlLIa61tnqP5/Kq6OoOQ95GxVgUAAMCijHqdvPlcnOT+4ygEAACA\npRt14pU9ZjdlcI28P07ylXEXBQAAwOKMek7ef+eWE63MuDLJE8dXDgAAAEsxash77Kz7NyXZmuTC\n1tr14y0JAACAxRp14pUzJl0IAAAASzfqSF6qavck906yb2ZN2NJaO33MdQEAALAIo0688r+SnJTk\nTnOsbnExdAAAgBVh1EsovDnJJ5P8aJI9kmwYus2eeRMAAIApGfVwzbsleXxr7WuTLAYAAIClGXUk\n73NJ7j7JQgAAAFi6UUfy3pjkL6tqY5JNSW4YXtlau3DchQEAALBwo4a807qf7+p+zlwYvWLiFQAA\ngBVj1JB3z4lWAQAAwFiMejH0zZMuBAAAgKUbdeKVVNXDq+oDVfWFqrpz1/b07hp6AAAArAAjhbyq\n+tUkH0myNYNDN3fvVu2R5MWTKQ0AAICFGnUk76VJntNa++0kNw61/2eSw8deFQAAAIsyasj7sSSf\nnqP92iR7jq8cAAAAlmLUkHdFkh+do/3BSb42vnIAAABYilFD3tuTvLGq7p/BdfH2q6onJjk+yQmT\nKg4AAICFGfU6ea9JsncG5+CtT/KZJDuSvKm19sYJ1QYAAMACjXqdvJbk96vqj5PcJ4MRwE2ttWsm\nWRwAAAALM1LIq6rnJDm5tbYtg1E8AAAAVqBRz8l7ZZIrquq0qjqmqnbf1QYAAAAsv1FD3oFJHp/k\nuiTvTHJlVb2tqh42oboAAABYhJFCXmttR2vtX1prT02yX5LnJrlTkjOq6pIJ1gcAAMACjDq75s1a\na9+rqjOS7JXkkCT3HHdRAAAALM6oh2umqjZU1ZOr6p+SXJbk95N8KMm9J1UcAAAACzPq7JrvTvK4\nJDcmeX+SR7bW/mOShQEAALBwox6uuSHJsUn+ubV2/QTrAQAAYAlGvRj6MZMuBAAAgKVbyDl5v1lV\nZ1fVt6vqkK7t96vq8ZMqDgAAgIUZKeRV1XOT/FmS92Vw6ObMdlcnef5kSgMAAGChRh3Je26SZ7XW\nXpvB5Cszzo7ZNQEAAFaMUUPeXZN8cY72HyS5zfjKAQAAYClGDXmXJPnJOdqPTHLR2KoBAABgSUa9\nhMIbkry5qtYnqST3q6pfTfKyJL89qeIAAABYmFEvoXBCVd06yd8k2SODCViuTvLi1tq7J1gfAAAA\nCzDqSF5aa3+d5K+r6s4ZHOb5jdZam1hlAAAALNjI18mb0Vr7Zmvt6621VlW7V9ULJlEYAAAAC7fL\nkFdVe1bVI6rqoVVVXdutquo5Sb6W5JUTrhEAAIAR7fRwzar6qSSnJ7ljkpbkP6vq6UlOTbJnkjcm\nOWHCNQIAADCiXY3k/WmS/0jygCR/m+TBSc5I8uYkd22t/WVr7drJlggAAMCodjXxyuFJHt5a21RV\nFyX5nSQva62dPPnSAAAAWKhdjeTdMcmVSdJa+26S7yY5e9JFAQAAsDi7GslrSTZU1R4ZXAS9Jdm9\nu//DB7X2vQnVBwAAwALsKuRVBjNoDt8/b47HrRtbRQAAACzarkLeY5elCgAAAMZipyGvtXbGchUC\nAADA0u1qJO8WqmrvJPtm1oQtrbULx1kUAAAAizNSyKuqeyf5hyQ/MdOUwSQsMz+dkwcAALACjDqS\n97Yk1yR5VJLLMgh2AAAArDCjhrz7JLlfa23zJIsBAABgaXZ1MfQZFybZZ5KFAAAAsHSjhrwXJfnz\nqnpIVd2hqvYYvk2yQAAAAEY36uGan+h+fmqe9SZeAQAAWAFGDXkuig4AALAKjBTyXBQdAABgdRj5\nYujdhdCfk+SwDC6hcEGSE1pr355QbQAAACzQSBOvVNUDk3w1g5B36yQ/kuR3knylqn5qcuUBAACw\nEKOO5L0uyWlJntVauzFJqmq3DC6S/oYkD5lMeQAAACzEqCHv/kmeORPwkqS1dmNV/UWSsyZSGQAA\nAAs26nXyrkty0Bztd+7WAQAAsAKMGvLel+TtVXVMVe3f3X4lyd916wAAAFgBRj1c80VJ1ic5OT8M\nhjdlcE7ecaM8QVW9I8kvJrmqtXbvrm3vJO9NckiSS5I8obV2zYg1AQAAMMtII3mtte+31n4rycYk\nD+puG1trv91a+/6Ir/XOJI+Z1fbiJB9vrd0jyce7+wAAACzSqIdrJklaa9taa5/vbtsWuO2nk8y+\npt5RSU7slk9McvRCnhMAAIBbmvdwzap6XwYzal7bLc+rtfaERb7+fq21y7vlK5Lst5N6np3k2Uly\n8MEHL/LlAAAA+m1nI3k7krRu+abu/ny3JWuttaHXm2v9Ca21I1prR2zcuHEcLwkAANA7847ktdae\nPLT8pAm9/pVVtX9r7fKq2j/JVRN6HQAAgDVhpHPyquotVXXbOdr3qKq3LOH1P5zk2G752CQfWsJz\nAQAArHmjTrzyW0n2mKN9j3Tnye1KVZ2U5L+SHFpV36yqZyT58ySPqqqLkzyyuw8AAMAi7fQ6eVW1\nR5Lqbhu6+zPWJXl0kq2jvNDw4Z+zPGKU7QEAANi1XV0M/b8zmAylJfnaPI/507FWBAAAwKLtKuQ9\nNoNRvNOT/FqSa4bWXZ/kktba/5tQbQAAACzQTkNea+2MJKmqeyb5cneZAwAAAFaoUSdeeViS/3EZ\nhap6clU9a6wVAQAAsGijhrwXJblijvYt3ToAAABWgFFD3kFJ5jr37utJDh5fOQAAACzFqCHvqiT3\nmaP9J5N8a3zlAAAAsBSjhryTk/xVVf1s/dBDk7wxyXsnVx4AAAALsatLKMz4P0nukeRTGVw6IUnW\nJ/lIkj+aQF0AAAAswkghr7X2gySPr6r7JLlv13xOa+38iVUGAADAgo06kpckaa1tSrJpQrUAAACw\nRCOHvKo6JMkvZzCb5u7D61prvzPWqgAAAFiUkUJeVT0qyYeSbE5yryRfTHK3JOuSnDmx6gAAAFiQ\nUWfXfE2S17bWDk/ygyRPzDWmP/kAABMgSURBVGBE71NJPjyh2gAAAFigUUPejyd5d7d8Y5INrbXv\nJnl5khdNojAAAAAWbtSQ99388Dy8y5PcvVtuSfYZd1EAAAAszqgTr5yZ5GeSXJTkX5McX1X3THJM\nnJMHAACwYowa8o5Lcttu+RVJ9kryjCRfTvK7E6gLAACARRj1Yuibh5avS/IbE6sIAACARRvpnLyq\n2quq9hq6f2hVvayqHj+50gAAAFioUSde+UCSX0mSqto7yX8meXqSf6iq35tMaQAAACzUqCHvvhkE\nu2Qw2cqlSe6R5NgkvzOBugAAAFiEUUPehiTXdcuPSvKh1lrLYGbNgydRGAAAAAs3asj7apJfqKp9\nkzw6yUe79n2TXDuJwgAAAFi4UUPeq5P8VZLLkpzTWvuvrv1RSc6dRGEAAAAs3KiXUHhvVf1XkgOT\nfH5o1WeS/NMkCgMAAGDhRr0YelprX0/y9Vltnxl7RQAAACzayCGvqo5K8ogMzsO7xWGerbUnjLku\nAAAAFmHUi6G/JskHM7iUQpLsmHUDAABgBRh1JO83kjyttfaPkywGAACApRl1ds3dk3xukoUAAACw\ndKOGvLcneeIkCwEAAGDpRj1cc7ckx1XVI5Kcl+SG4ZWttT8Yd2EAAAAs3Kgh76eTfCnJHkkeNGtd\nG2tFAAAALNqoF0P/6UkXAgAAwNKNek4eAAAAq8BCLob+M0melOTgDGbbvFlr7efHXBcAAACLMOrF\n0H8tySeTHJTksUmuT3JIkp9JsmVCtQEAALBAox6u+ZIkz2+tPT6DgPfCJPdK8r4kV0yoNgAAABZo\n1JB3tyT/0i1fn+Q2rbWW5A1JnjmJwgAAAFi4UUPeNUlu1y1vSXJYt3yHJLcZd1EAAAAszqgTr3wm\nycOTbErywSRvqqqHJTkyyb9PpjQAAAAWatSQ93tJNnTLr+5+PjjJ6UleMe6iAAAAWJxdhryq2i3J\nL2YQ6NJa25HkVROuCwAAgEXY5Tl5rbUbk7w5ya0nXw4AAABLMerEK2cm+clJFgIAAMDSjXpO3puT\nvK6qDkhydpLvDq9srV047sIAAABYuFFD3vu6n2/pfrbuZ3XL68ZZFAAAAIszasi750SrAAAAYCx2\nGvKq6h1Jnt9a27xM9QAAALAEu5p45dj88Pp4AAAArHC7Cnm1LFUAAAAwFqNcQqHt+iEAAACsBKNM\nvHJF1c4H9FprZtcEAABYAUYJec9Osm3ShQAAALB0o4S8j7TWrpp4JQAAACzZrs7Jcz4eAADAKmJ2\nTQAAgB7Z6eGarbVRZt8EAABghRDiAAAAekTIAwAA6BEhDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgR\nIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEeE\nPAAAgB4R8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8AACAHhHy\nAAAAekTIAwAA6BEhDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgD\nAADoESEPAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgRIQ8A\nAKBHhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEd2m3YB\nSVJVlyS5LsmOJDe21o6YbkUAAACr04oIeZ2fa61dPe0iAAAAVjOHawIAAPTISgl5LclHq+rsqnr2\nXA+oqmdX1VlVddbWrVuXuTwAAIDVYaWEvIe01u6X5LFJnltVD539gNbaCa21I1prR2zcuHH5KwQA\nAFgFVkTIa61t6X5eleTUJA+YbkUAAACr09RDXlXdpqpuN7Oc5NFJzp9uVQAAAKvTSphdc78kp1ZV\nMqjnH1tr/zrdkgAAAFanqYe81trXkvzktOsAAADog6kfrgkAAMD4CHkAAAA9IuQBAAD0iJAHAADQ\nI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECP\nCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i\n5AEAAPSIkAcAANAjQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQ\nBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0Ie\nAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECPCHkA\nAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEA\nAPSIkAcAANAjQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA\n0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0IeAABA\njwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECPCHkAAAA9\nIuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNCHgAAQI8IeQAAAD0i5AEAAPSI\nkAcAANAjQh4AAECPCHkAAAA9IuQBAAD0iJAHAADQI0IeAABAjwh5AAAAPSLkAQAA9IiQBwAA0CNC\nHgAAQI8IeQAAAD0i5AEAAPSIkAcAANAjQh4AAECP7DbtApKkqh6T5E1J1iV5W2vtz6dc0oIc8uJ/\nnnYJAADAEl3y578w7RLGYuojeVW1LsnfJHlsksOSPLmqDptuVaMT8AAAoB/68rf91ENekgck+Upr\n7WutteuTnJzkqCnXBAAAsCqthJB3YJJvDN3/Ztd2C1X17Ko6q6rO2rp167IVBwAAsJqshJA3ktba\nCa21I1prR2zcuHHa5QAAAKxIKyHkbUly0ND9O3dtAAAALNBKCHmfT3KPqrprVe2e5ElJPjzlmkbW\nlxl4AABgrevL3/ZTv4RCa+3GqnpekjMyuITCO1prF0y5rAXpy4cBAABY/aYe8pKktXZ6ktOnXQcA\nAMBqtxIO1wQAAGBMhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8AACAHhHyAAAAekTIAwAA6BEh\nDwAAoEeEPAAAgB4R8gAAAHpEyAMAAOgRIQ8AAKBHhDwAAIAeEfIAAAB6RMgDAADoESEPAACgR4Q8\nAACAHhHyAAAAeqRaa9OuYcGqamuSS6ddxxz2SXL1tItgTvpmZdM/K5e+Wdn0z8qlb1Y2/bNy6ZvR\n3aW1tnGuFasy5K1UVXVWa+2IadfB/6RvVjb9s3Lpm5VN/6xc+mZl0z8rl74ZD4drAgAA9IiQBwAA\n0CNC3nidMO0CmJe+Wdn0z8qlb1Y2/bNy6ZuVTf+sXPpmDJyTBwAA0CNG8gAAAHpEyAMAAOgRIW8M\nquoxVbW5qr5SVS+edj1rRVUdVFWfqKoLq+qCqnp+1/7KqtpSVed2t58f2uYlXT9trqojh9r14ZhV\n1SVVtanrg7O6tr2r6mNVdXH3c6+uvarqr7r9f15V3W/oeY7tHn9xVR07rffTJ1V16ND349yquraq\nXuC7Mx1V9Y6quqqqzh9qG9t3paru330Xv9JtW8v7Dle3efrn+Kr6UtcHp1bVnl37IVW1feg79Nah\nbebsh/n6ml2bp2/G9nusqu5aVZ/r2t9bVbsv37tb/ebpn/cO9c0lVXVu1+67M26tNbcl3JKsS/LV\nJHdLsnuSLyY5bNp1rYVbkv2T3K9bvl2SLyc5LMkrk7xojscf1vXPrZPcteu3dfpwYv1zSZJ9ZrX9\nRZIXd8svTvLabvnnk/xLkkryoCSf69r3TvK17ude3fJe035vfbp1n/8rktzFd2dqffDQJPdLcv5Q\n29i+K0nO7B5b3baPnfZ7Xk23efrn0Ul265ZfO9Q/hww/btbzzNkP8/W126L7Zmy/x5K8L8mTuuW3\nJvntab/n1XSbq39mrX9dkpd3y747Y74ZyVu6ByT5Smvta62165OcnOSoKde0JrTWLm+tfaFbvi7J\nRUkO3MkmRyU5ubX2g9ba/0vylQz6Tx8un6OSnNgtn5jk6KH2d7WBzybZs6r2T3Jkko+11r7dWrsm\nyceSPGa5i+65RyT5amvt0p08xndnglprn07y7VnNY/mudOtu31r7bBv8JfSuoediBHP1T2vto621\nG7u7n01y5509xy76Yb6+Zhfm+e7MZ0G/x7rRoocn+UC3vb5ZoJ31T7d/n5DkpJ09h+/O4gl5S3dg\nkm8M3f9mdh40mICqOiTJ4Uk+1zU9rzuM5h1Dw/fz9ZU+nIyW5KNVdXZVPbtr26+1dnm3fEWS/bpl\nfTM9T8ot/5H13VkZxvVdObBbnt3O+PxmBqMLM+5aVedU1aeq6me7tp31w3x9zeKN4/fYHZNsGwrz\nvjvj9bNJrmytXTzU5rszRkIeq15V3TbJB5O8oLV2bZK/TXL3JPdNcnkGhwOw/B7SWrtfkscmeW5V\nPXR4Zfc/cq7hMkXd+SWPS/L+rsl3ZwXyXVm5quqlSW5M8p6u6fIkB7fWDk/ywiT/WFW3H/X59PVY\n+D22Ojw5t/wPRt+dMRPylm5LkoOG7t+5a2MZVNX6DALee1prpyRJa+3K1tqO1tpNSf4ug0Mxkvn7\nSh9OQGttS/fzqiSnZtAPV3aHXswcgnFV93B9Mx2PTfKF1tqVie/OCjOu78qW3PJQQn00JlX19CS/\nmOQp3R+Y6Q4F/Fa3fHYG53r9WHbeD/P1NYswxt9j38rgcOjdZrWzRN0+/eUk751p890ZPyFv6T6f\n5B7dDEy7Z3Do04enXNOa0B3P/fYkF7XWXj/Uvv/Qwx6fZGZWpw8neVJV3bqq7prkHhmczKsPx6yq\nblNVt5tZzmCSgvMz2K8zs/4dm+RD3fKHkzytBh6U5DvdIRhnJHl0Ve3VHXLz6K6N8bjF/6T67qwo\nY/mudOuuraoHdb8znzb0XCxSVT0myR8keVxr7XtD7Rural23fLcMvitf20U/zNfXLMK4fo91wf0T\nSX6l217fjM8jk3yptXbzYZi+OxMw7Zlf+nDLYLazL2fwvw4vnXY9a+WW5CEZDM2fl+Tc7vbzSf4h\nyaau/cNJ9h/a5qVdP23O0Axz+nDsfXO3DGYo+2KSC2b2aQbnOHw8ycVJ/i3J3l17Jfmbbv9vSnLE\n0HP9ZgYnyH8lyW9M+7315ZbkNhn8T/Udhtp8d6bTFydlcKjSDRmcb/KMcX5XkhyRwR+6X03y5iQ1\n7fe8mm7z9M9XMjiPa+bfnrd2jz2m+513bpIvJPmlXfXDfH3ttui+Gdvvse7fsjO7/n5/kltP+z2v\npttc/dO1vzPJc2Y91ndnzLeZnQQAAEAPOFwTAACgR4Q8AACAHhHyAAAAekTIAwAA6BEhDwAAoEeE\nPADWlKp6Z1X90xKf4/yqeuWYSgKAsdpt2gUAwDJ7fgbXmwOAXhLyAFhTWmvfmXYNADBJDtcEYE0Z\nPlyzqj5ZVW+pqtdU1dVVdVVV/WVV3Wro8ftW1YeqantVXVpVvznHc96hqk7otr+uqj5VVUcMrX97\nVV1QVRu6++uq6j+WetgoAMxFyANgrXtKkhuT/EyS5yV5QZInDq1/Z5IfTfLIJEcneVqSQ2ZWVlUl\n+eckByb5xSSHJ/l0kn+vqv27h/1ekvVJ/rK7/9Ik90jyPwIjACyVwzX5/9u5nxcf4jiO48+Xi80d\n5aC0RXKwUaJ2lZxW8Q9IXPaiXNwciMMe+AOUnH2VpOTAQW5fB8rBQVby47KFXJT2IPt22PlqWnYP\nsnuYeT5q6vNzms9pejWfz0hS372qqktN+U2SGeAocDvJTmAamKyqIUCS08C71vwjwASwuaoWmraL\nSY4Dp4BrVfU9yUlgmOQrcAE4UVWf13x1kqTeMeRJkvru5bL6PLClKe8GFoFno86q+phkvjV+P7AJ\n+LL0Ue+3MWC8Ne95klngMnC9qh7+rwVIktRmyJMk9d2PZfXiz+MMtcr8DcAnYOovfd9GhWZb5yTw\nExhPkqpa7b6SJP0Tz+RJkrSy1yy9Kw+MGpJsB7a1xrwAtgKLVfV22dXejnke2AccBg4C59b86SVJ\nvWTIkyRpBVU1BzwCbiQ5lGSCpR+xLLSGPQaGwP0k00l2NGOvJJkCSLIXmAVmquopcBa4mmTPeq5H\nktQPhjxJklZ3BngPPAEeAAPgw6iz2XJ5rOm/CcwBd4BdwHySMeAWMKiqe82cAXAXGCTZuF4LkST1\nQzwOIEmSJEnd4Zc8SZIkSeoQQ54kSZIkdYghT5IkSZI6xJAnSZIkSR1iyJMkSZKkDjHkSZIkSVKH\nGPIkSZIkqUMMeZIkSZLUIb8AkFJFJ0pL9TMAAAAASUVORK5CYII=\n",
            "text/plain": [
              "<Figure size 1080x720 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab_type": "code",
        "outputId": "6fb592ce-67a7-44c9-bbb3-3e505ed8f8aa",
        "id": "yTLpjO2JOHCF",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 51
        }
      },
      "source": [
        "non_zero_instance = pd.notnull(train_df[\"totals.transactionRevenue\"]).sum()\n",
        "print(\"Number of instances in train set with non-zero revenue : \", non_zero_instance, \" and ratio is : \", non_zero_instance / train_df.shape[0])\n",
        "non_zero_revenue = (grouped_df_sum[\"totals.transactionRevenue\"]>0).sum()\n",
        "print(\"Number of unique customers with non-zero revenue : \", non_zero_revenue, \"and the ratio is : \", non_zero_revenue / train_df.shape[0])"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Number of instances in train set with non-zero revenue :  193  and ratio is :  0.00965\n",
            "Number of unique customers with non-zero revenue :  189 and the ratio is :  0.00945\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CBPJDcBxZOg4",
        "colab_type": "code",
        "outputId": "a9247a94-a285-488a-dbbd-2060a0f4b55e",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 65
        }
      },
      "source": [
        "print(\"Number of unique visitors in train set : \",train_df.fullVisitorId.nunique(), \" out of rows : \",train_df.shape[0])\n",
        "print(\"Number of unique visitors in test set : \",test_df.fullVisitorId.nunique(), \" out of rows : \",test_df.shape[0])\n",
        "print(\"Number of common visitors in train and test set : \",len(set(train_df.fullVisitorId.unique()).intersection(set(test_df.fullVisitorId.unique())) ))"
      ],
      "execution_count": 44,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Number of unique visitors in train set :  18384  out of rows :  20000\n",
            "Number of unique visitors in test set :  1855  out of rows :  2000\n",
            "Number of common visitors in train and test set :  7\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XKZxKzbCbOAJ",
        "colab_type": "text"
      },
      "source": [
        "Charting the Transactions and Revenue per Date"
      ]
    }
  ]
}