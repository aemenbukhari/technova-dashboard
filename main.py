#   Subject: Decision Support Systems
#    assignment #1
#    Student Name: Aemen Hasan
#    enrollment no. 02-243241-008
#use streamlit run main.py on terminal




import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Load Data
# ------------------------
df = pd.read_csv("technova_data.csv")
#df is a pandas dataframe
# Ensure numeric columns (fixes wrong On-Time/Delayed calculation)
df["Deadline_Days"] = df["Deadline_Days"].astype(int)
df["Actual_Days"] = df["Actual_Days"].astype(int)
df["Hours_Worked"] = df["Hours_Worked"].astype(int)
df["Project_Cost"] = df["Project_Cost"].astype(float)
df["Project_Revenue"] = df["Project_Revenue"].astype(float)

# Calculates On-time/Delayed correctly
#This line of code adds a new column "Status" to our DataFrame
# based on a condition comparing Actual_Days and Deadline_Days.
df["Status"] = df.apply(
  lambda x: "On-Time" if x["Actual_Days"] <= x["Deadline_Days"] else "Delayed",
   axis=1
)

#df.apply(...) applies a function row by row (because axis=1 means “work across columns of each row”).
#lambda x: ...This defines a tiny function that runs on each row.
# x represents one row of the DataFrame.


# Profit Calculation
df["Profit"] = df["Project_Revenue"] - df["Project_Cost"]
#pandas dataframe df's new column profit

# ------------------------
# Sidebar Filters
# ------------------------

st.sidebar.header("Filters")

#This code creates a multi-select filter inside the Streamlit sidebar
#so the user can choose one or more clients to display in the dashboard.
client_filter = st.sidebar.multiselect(  #st.sidebar.multiselect creates a multi-selection dropdown in the sidebar.
    "Select Client",   #Creates a multi-selection dropdown in the sidebar.
    options=df["Client"].unique(),#Looks at your DataFrame (df), Takes the Client column, Gets all unique client names as choices in the multi-select dropdown.
    default=df["Client"].unique() #This pre-selects all clients by default, so the dashboard initially shows all data.
)

team_filter = st.sidebar.multiselect(
    "Select Team Lead",
    options=df["Team_Lead"].unique(),
    default=df["Team_Lead"].unique()
)

# Apply filters
df_filtered = df[
    (df["Client"].isin(client_filter)) &
    (df["Team_Lead"].isin(team_filter))
]

# Handle case when user removes all filters
if df_filtered.empty:
    st.title("TechNova Software House — Performance Analytics Dashboard")
    st.warning("⚠️ No data available for the selected filters. Please select at least one Client or Team Lead.")
    st.stop()

# ------------------------
# KPI Section
# ------------------------
st.title("TechNova Software House — Performance Analytics Dashboard")

total_revenue = df_filtered["Project_Revenue"].sum()
avg_rating = df_filtered["Client_Rating"].mean()
on_time_percent = (df_filtered["Status"].value_counts().get("On-Time", 0) /
                   len(df_filtered)) * 100

col1, col2, col3 = st.columns(3)
#This function from the Streamlit library creates a horizontal layout with three equally spaced columns.
# It returns a list of three "container" objects, each representing one of these columns.

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Average Client Rating", f"{avg_rating:.2f} / 5")
col3.metric("% Projects On-Time", f"{on_time_percent:.1f}%")
#display a KPI-style metric box.

#draw a horizontal line (divider) on your dashboard.
st.markdown("---")
#st.markdown("---")
#syntax of markdown()
#st.markdown("# Heading 1")
#st.markdown("## Heading 2")
#st.markdown("### Heading 3")
#("""   """) allows multiline
#st.markdown("- Item 1\n- Item 2\n- Item 3") displays a bullet-point list in Streamlit using Markdown.

#-----------------------Section1 performance-----------------

st.subheader("1. Project Performance Analysis")
# ------------------------
# ROW 1 — Two Graphs
# ------------------------
g1_col, g2_col = st.columns(2)

# GRAPH 1: On-Time vs Delayed Projects
with g1_col:  #All the elements written inside this block should appear inside the container g1_col
   # st.subheader("2.2 Comparison of number of Ontime and delayed projects")
    # Count status values
    status_count = df_filtered["Status"].value_counts().reset_index()
    #This line is Pandas code that creates a small summary table
   # showing how many times each Status appears.
    status_count.columns = ["Status", "Count"]
    #simply renames the columns of the DataFrame status_count.
    # Color mapping
    color_map = {
        "On-Time": "brown",
        "Delayed": "grey"
    }
   #This line creates a Python dictionary called color_map
   # that assigns a specific color to each status category.

    fig1 = px.bar(
        status_count,
        x="Status",
        y="Count",
        title="On-Time vs Delayed Projects",
        color="Status",
        color_discrete_map=color_map,
        text="Count"
    )
   #creates a Plotly Express bar chart that compares On-Time vs Delayed project counts.

    fig1.update_layout(showlegend=False)
    fig1.update_traces(textposition="outside")
   #This moves the text labels (the Count values) outside the top of each bar. works well
   #when bars are too short to show the text labels inside the bar

    st.plotly_chart(fig1, use_container_width=True)
    #displays the Plotly figure in Streamlit.
#use_container_width=True means the chart will automatically expand to the full
#available width of the column or page , responsive layout.



# Graph 2: Planned vs Actual Days
with g2_col:

    fig2 = px.bar(  #plotly express function
        df_filtered,
        x="Project_ID",
        y=["Deadline_Days", "Actual_Days"],
        barmode="group",
        title="Planned vs Actual Days"
    )
    #creates a grouped bar chart comparing Deadline_Days vs Actual_Days for each project.
    st.plotly_chart(fig2, use_container_width=True)
   #This Streamlit function renders a Plotly figure in the dashboard.

# INSIGHTS SECTION
st.subheader("Key Performance Insights")

# -----------------------------
# INSIGHTS FOR GRAPH 1
# On-Time vs Delayed
# -----------------------------
status_count = df_filtered["Status"].value_counts()
#makes a summary table
total_projects = len(df_filtered)
on_time = status_count.get("On-Time", 0) #gives the number of times On-Time occurs. Value corresponding to on-Time
delayed = status_count.get("Delayed", 0)
#calculate percentages
on_time_pct = (on_time / total_projects * 100) if total_projects > 0 else 0
delayed_pct = (delayed / total_projects * 100) if total_projects > 0 else 0

st.markdown(f"""
### 
- **Total Projects:** {total_projects}
- **On-Time:** {on_time} ({on_time_pct:.1f}%)
- **Delayed:** {delayed} ({delayed_pct:.1f}%)
- {"Most projects are on schedule." if on_time > delayed else "⚠️ Most projects are getting delayed — requires attention."}
""")
#prints a summary section with bullet points. """makes multiline, f for formatted string
#st.markdown("---")
st.markdown("---")
# --------------Section2 related to profitability
# ------------------------
# Profitability (Cost vs Revenue)
# -----------------------#
st.subheader("2.1 Profit Margin per project")
fig3 = px.scatter(
    df_filtered,
    x="Project_Cost",
    y="Project_Revenue",
    color="Team_Lead",  #Each Team Lead gets a unique color.
    size="Profit",#The size of each bubble depends on profit
    hover_name="Project_ID",
    title="Project Profitability — Cost vs Revenue"
)
#This line creates a scatter plot (bubble chart) with
# Plotly Express to visualize project profitability using multiple dimensions at once.
st.plotly_chart(fig3, use_container_width=True)

#------------
# ------------------------
# Revenue vs Cost Bar Graph
# ------------------------

# Calculate Profit
df_filtered["Profit"] = df_filtered["Project_Revenue"] - df_filtered["Project_Cost"]

# Sort by Profit (Descending)
df_sorted = df_filtered.sort_values("Profit", ascending=False)


# Profit color logic: green for positive, red for negative
df_sorted["Profit_Color"] = df_sorted["Profit"].apply(lambda x: "brown" if x >= 0 else "teal")


# Revenue vs Cost Chart
fig_rev_cost = px.bar(
    df_sorted,
    x="Project_ID",
    y=["Project_Revenue", "Project_Cost"],
    barmode="group",
    title="Revenue and Cost vs Project ID(sorted by profit)"
)


# Profit Chart (Color-coded)
fig_profit = px.bar(
    df_sorted,
    x="Project_ID",
    y="Profit",
    title="Profit vs Project ID(Sorted by Profit)",
    color="Profit_Color",
    color_discrete_map={"green": "green", "red": "red"}  # Force correct colors
)

fig_profit.update_layout(showlegend=False)


# Show both graphs side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("2.2 Revenue vs Cost per project")
    st.plotly_chart(fig_rev_cost, use_container_width=True)

with col2:
    st.subheader("2.3 Profit per Project")
    st.plotly_chart(fig_profit, use_container_width=True)


# Insights Section
# INSIGHTS FOR GRAPH : Profitability (Cost vs Revenue)
st.subheader(" Key Profitability Insights")

# Basic Stats
avg_cost = df_filtered["Project_Cost"].mean()
avg_revenue = df_filtered["Project_Revenue"].mean()
avg_profit = df_filtered["Profit"].mean()

# Loss-making projects
loss_projects = df_filtered[df_filtered["Profit"] < 0]
loss_count = len(loss_projects)

# Most profitable project
top_project = df_filtered.loc[df_filtered["Profit"].idxmax()]

# Correlation between cost and revenue
#corr() computes the Pearson correlation coefficient, which measures:
# How strongly two variables move together
#It returns a value between -1 and +1:
#Correlation	Meaning
#+1.0	Perfect positive relationship (higher cost → higher revenue)
#0.0	No relationship
#-1.0	Perfect negative relationship (higher cost → lower revenue)
corr_cost_rev = df_filtered["Project_Cost"].corr(df_filtered["Project_Revenue"])
#we are measuring do projects that cost more also generate more revenue?
#making sub headings
st.markdown(f"""    
### 
- **Average Cost:** ${avg_cost:,.0f}  
- **Average Revenue:** ${avg_revenue:,.0f}  
- **Average Profit:** ${avg_profit:,.0f}  
### 
- **Most Profitable Project:** `{top_project['Project_ID']}`  
  - Profit: ${top_project['Profit']:,.0f}  
  - Revenue: ${top_project['Project_Revenue']:,.0f}  
- **Loss-Making Projects:** {loss_count}
### 
- **Cost–Revenue Correlation:** {corr_cost_rev:.2f}
- {"Higher costs are generally leading to higher revenues." if corr_cost_rev >= 0.6 else "⚠️ Higher spending does not strongly guarantee higher revenue."}  
- {"Some projects are running at a loss — investigate cost overruns or pricing issues." if loss_count > 0 else "All projects are profitable — strong financial performance."}
""")

st.markdown("---")
#st.markdown("---")

#--------Section 3: Developers/Team Leads related-------------------
# ------------------------
# Team Productivity (Hours by Team Lead)
# ------------------------
st.subheader("3.1 Team Utilization/Developer workload")
hours_by_team = df_filtered.groupby("Team_Lead")["Hours_Worked"].sum().reset_index()

fig4 = px.pie(
    hours_by_team,
    names="Team_Lead",
    values="Hours_Worked",
    title="Team Productivity — Hours Worked by Team Lead"
)
st.plotly_chart(fig4, use_container_width=True)

# INSIGHTS FOR GRAPH: Team Utilization / Developer Workload
st.subheader("Team Utilization Insights")

total_hours = hours_by_team["Hours_Worked"].sum()

# Identify most & least loaded team leads
most_loaded = hours_by_team.loc[hours_by_team["Hours_Worked"].idxmax()]
least_loaded = hours_by_team.loc[hours_by_team["Hours_Worked"].idxmin()]
#use the pandas library in Python to find the rows corresponding to the
# maximum and minimum values in the "Hours_Worked" column of a DataFrame named hours_by_team

# Workload distribution
hours_by_team["Percentage"] = (hours_by_team["Hours_Worked"] / total_hours * 100).round(1)
#Rounds the percentage to 1 decimal place.
st.markdown(f"""
### 
- **Total Hours Worked Across All Teams:** {total_hours:,.0f}
### 
- **Most Loaded Team Lead:** `{most_loaded['Team_Lead']}`  
  Hours Worked: **{most_loaded['Hours_Worked']:,.0f}**  
  Share of Total: **{(most_loaded['Hours_Worked'] / total_hours * 100):.1f}%**
- **Least Loaded Team Lead:** `{least_loaded['Team_Lead']}`  
  Hours Worked: **{least_loaded['Hours_Worked']:,.0f}**  
  Share of Total: **{(least_loaded['Hours_Worked'] / total_hours * 100):.1f}%**
""")

#hourly rate vs team lead
#This shows which team lead charges the highest or lowest rates.
st.subheader("3.2 Hourly Rate per developer")
hourly_by_team = df_filtered.groupby("Team_Lead")["Hourly_Rate"].mean().reset_index()
#.reset_index() converts this index back into a regular column in the output DataFrame.
# This makes the final result a standard DataFrame with columns named "Team_Lead" and "Hourly_Rate"
# (or similar, depending on how pandas names it), rather than having "Team_Lead" as the index label.



fig_hr1 = px.bar(
    hourly_by_team,
    x="Team_Lead",
    y="Hourly_Rate",
    title="Average Hourly Rate by Team Lead",
    text_auto=True
)
st.plotly_chart(fig_hr1, use_container_width=True)


# ✅ INSIGHTS FOR GRAPH: Hourly Rate per Developer
st.subheader("Hourly Rate Insights")

overall_avg_rate = hourly_by_team["Hourly_Rate"].mean()

# Highest & lowest paid teams
highest_rate = hourly_by_team.loc[hourly_by_team["Hourly_Rate"].idxmax()]
lowest_rate = hourly_by_team.loc[hourly_by_team["Hourly_Rate"].idxmin()]

rate_gap = highest_rate["Hourly_Rate"] - lowest_rate["Hourly_Rate"]

st.markdown(f"""
### 
- **Overall Average Hourly Rate:** ${overall_avg_rate:,.2f}
###
- **Developer with highest Average Rate:** `{highest_rate['Team_Lead']}`  
  Rate: **${highest_rate['Hourly_Rate']:,.2f}**
- **Developer with lowest Average Rate:** `{lowest_rate['Team_Lead']}`  
  Rate: **${lowest_rate['Hourly_Rate']:,.2f}**
- **Rate Gap:** ${rate_gap:,.2f} difference between highest and lowest teams
### 
- {"⚠️ Large variation in hourly rates — possible differences in seniority or billing structure." 
    if rate_gap > (overall_avg_rate * 0.25) 
    else "Hourly rates are fairly consistent across team leads."}
- Teams with higher hourly rates may correlate with **higher revenue projects** or **specialized skills**.
""")

st.markdown("---")
#st.markdown("---")
#-------------------section 4----------------------------------------------#
# ------------------------
# Client Satisfaction Heatmap
# ------------------------
st.subheader("4. Client Satisfaction Heatmap")

heatmap_data = df_filtered.pivot_table(
    values="Client_Rating",
    index="Client",
    columns="Project_ID"
)

fig5 = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Client Rating by Project ID"
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------------------
# GRAPH : Client Satisfaction Heatmap (Team Lead)
# -------------------------------------


pivot_table = df_filtered.pivot_table(
    values="Client_Rating",  # Fill the table with Client_Rating values.
    index="Client",   #Make each Client the row of the table
    columns="Team_Lead",  #columns="Team_Lead"
    aggfunc="mean"   #If a client has multiple projects with the same team lead, average their ratings
)
#This function converts our data into a matrix (table) that shows the average client rating for each team lead,
# organized by client.
#three columns: client, team lead, rating
fig4 = px.imshow(
    pivot_table,
    text_auto=True,
    aspect="auto",
    title="Client Rating by Team Lead"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ---------------------------------------
# INSIGHTS FOR CLIENT SATISFACTION HEATMAPS
# ---------------------------------------
st.subheader("Client Satisfaction Insights")

# -----------------------------------
# Insights for Heatmap 1: Ratings by Project ID
# -----------------------------------

avg_rating_overall = df_filtered["Client_Rating"].mean()

# Client averages
client_avg = df_filtered.groupby("Client")["Client_Rating"].mean()
max_client_rating = client_avg.max()
min_client_rating = client_avg.min()
best_clients = client_avg[client_avg == max_client_rating].index.tolist()
worst_clients = client_avg[client_avg == min_client_rating].index.tolist()

# Project averages
project_avg = df_filtered.groupby("Project_ID")["Client_Rating"].mean()
max_project_rating = project_avg.max()
min_project_rating = project_avg.min()
best_projects = project_avg[project_avg == max_project_rating].index.tolist()
worst_projects = project_avg[project_avg == min_project_rating].index.tolist()

st.markdown(f"""
### Heatmap 1: Client Rating by Project ID
- **Overall Average Rating:** {avg_rating_overall:.2f}
- **Highest Satisfaction Clients:** {", ".join(best_clients)} (Avg Rating: {max_client_rating:.2f})
- **Lowest Satusfaction Clients:** {", ".join(worst_clients)} (Avg Rating: {min_client_rating:.2f})
- **Best Projects by client rating:** {", ".join(best_projects)} (Rating: {max_project_rating:.2f})  
- **Worst Projects by client rating:** {", ".join(worst_projects)} (Rating: {min_project_rating:.2f})
**Insight:**  
- Clients with lower ratings may be facing communication, timeline, or quality issues.  
- Projects with consistently high ratings indicate strong delivery performance.
""")

# -----------------------------------
# Insights for Heatmap 2: Ratings by Team Lead
# -----------------------------------

team_avg = df_filtered.groupby("Team_Lead")["Client_Rating"].mean()
max_team_rating = team_avg.max()
min_team_rating = team_avg.min()
best_teams = team_avg[team_avg == max_team_rating].index.tolist()
worst_teams = team_avg[team_avg == min_team_rating].index.tolist()
rating_gap = max_team_rating - min_team_rating

st.markdown(f"""
### Heatmap 2: Client Rating by Team Lead
- **Top-Rated Team Leads:** {", ".join(best_teams)} (Avg Rating: {max_team_rating:.2f})
- **Lowest-Rated Team Leads:** {", ".join(worst_teams)} (Avg Rating: {min_team_rating:.2f})
- **Rating Gap:** {rating_gap:.2f}
**Insight:**  
- {"Large rating variance detected — team consistency needs improvement." 
    if rating_gap >= 1 else 
    "Client experience is fairly consistent across team leads."}
""")


