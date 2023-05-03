import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from flask import Flask, request, render_template

# Create Flask app
app = Flask(__name__)

# Create endpoint to upload CSV file
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)

        # Get the list of column names
        columns = df.columns.tolist()
        columns.remove('Year')
        columns.remove('Area_Name')

        # Create a list of plots for each column
        plots = []
        for column in columns:
            # Skip over any non-numeric columns
            if not pd.api.types.is_numeric_dtype(df[column]):
                continue

            # Create a bar plot of the total number of crimes by state
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(x='Area_Name', y=column, data=df)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            plt.title(f'{column.title()} by State')

            # Save plot to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Encode plot to base64 string
            plot_data = base64.b64encode(buffer.getvalue()).decode()

            # Create HTML img tag with base64 encoded plot
            plot_html = f'<img src="data:image/png;base64,{plot_data}" style="max-width:100%;height:auto;">'

            # Append plot to the list
            plots.append(plot_html)

            # Close the plot
            plt.close()

            # Create a bar plot of the total number of crimes by year
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(x='Year', y=column, data=df)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            plt.title(f'{column.title()} by Year')

            # Save plot to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Encode plot to base64 string
            plot_data = base64.b64encode(buffer.getvalue()).decode()

            # Create HTML img tag with base64 encoded plot
            plot_html = f'<img src="data:image/png;base64,{plot_data}" style="max-width:100%;height:auto;">'

            # Append plot to the list
            plots.append(plot_html)

            # Close the plot
            plt.close()

        # Concatenate the list of plots and return as a string
        return ''.join(plots)

    # Render file upload form
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
