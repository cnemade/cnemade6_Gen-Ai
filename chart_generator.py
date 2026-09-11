import matplotlib.pyplot as plt

def generate_chart(df, chart_type, x_col, y_col):
    plt.figure()

    if chart_type == "bar":
        df.groupby(x_col)[y_col].sum().plot(kind='bar')

    elif chart_type == "line":
        df.groupby(x_col)[y_col].sum().plot(kind='line')

    elif chart_type == "pie":
        df.groupby(x_col)[y_col].sum().plot(kind='pie', autopct='%1.1f%%')

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type.upper()} Chart")

    return plt