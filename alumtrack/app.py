import streamlit as st
import sqlite3
import pandas as pd
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AlumTrack",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "alumtrack.db")


def get_connection():
    return sqlite3.connect(DATABASE)


def get_all_alumni():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM alumni ORDER BY id",
        conn
    )

    conn.close()

    return df


def update_alumni(
    alumni_id,
    company,
    position,
    industry,
    location,
    status
):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alumni
        SET company = ?,
            position = ?,
            industry = ?,
            location = ?,
            status = ?
        WHERE id = ?
    """, (
        company,
        position,
        industry,
        location,
        status,
        alumni_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# LOAD DATABASE
# =========================================================

alumni = get_all_alumni()

if alumni.empty:

    st.error("No alumni found in database.")

    st.info(
        "Please run: python setup_database.py"
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 AlumTrack")

    st.caption(
        "Beyond Graduation"
    )

    st.divider()

    st.info(
        f"👥 {len(alumni)} Alumni Connected"
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👥 Alumni Directory",
            "🔍 Search Alumni",
            "👤 Alumni Profile",
            "📈 Career History",
            "✏️ Update Career"
        ]
    )

    st.divider()

    st.caption(
        "AlumTrack • Alumni Intelligence Platform"
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🎓 AlumTrack")
    st.subheader("Beyond Graduation")
    st.caption(
        "Real-time alumni intelligence dashboard"
    )

    st.divider()

    # -------------------------
    # Metrics
    # -------------------------

    total = len(alumni)

    working = len(
        alumni[
            alumni["status"] == "Working"
        ]
    )

    entrepreneurs = len(
        alumni[
            alumni["status"] == "Entrepreneur"
        ]
    )

    verified = len(
        alumni[
            alumni["verified"] == "Verified"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Total Alumni",
            total
        )

    with col2:
        st.metric(
            "💼 Working",
            working
        )

    with col3:
        st.metric(
            "🚀 Entrepreneurs",
            entrepreneurs
        )

    with col4:
        st.metric(
            "✓ Verified",
            verified
        )

    st.divider()

    # -------------------------
    # Insights
    # -------------------------

    st.subheader("📊 Alumni Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 🏢 Companies")

        company_data = (
            alumni["company"]
            .value_counts()
            .head(10)
        )

        st.bar_chart(
            company_data
        )

    with col2:

        st.write("### 🎓 Graduation Years")

        year_data = (
            alumni["graduation_year"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            year_data
        )

    st.divider()

    st.subheader("🌎 Alumni Locations")

    location_data = (
        alumni["location"]
        .value_counts()
    )

    st.bar_chart(
        location_data
    )

    st.divider()

    # -------------------------
    # Recent Alumni Table
    # -------------------------

    st.subheader("👥 All Alumni")

    display_data = alumni[
        [
            "name",
            "course",
            "graduation_year",
            "company",
            "position",
            "location",
            "status"
        ]
    ].copy()

    display_data.columns = [
        "Name",
        "Course",
        "Graduation Year",
        "Company",
        "Position",
        "Location",
        "Status"
    ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# ALUMNI DIRECTORY
# =========================================================

elif page == "👥 Alumni Directory":

    st.title("👥 Alumni Directory")

    st.caption(
        "Browse all registered alumni"
    )

    st.divider()

    # -------------------------
    # Filters
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        course_filter = st.selectbox(
            "🎓 Course",
            ["All"] +
            sorted(
                alumni["course"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with col2:

        industry_filter = st.selectbox(
            "🏭 Industry",
            ["All"] +
            sorted(
                alumni["industry"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with col3:

        status_filter = st.selectbox(
            "📊 Status",
            ["All"] +
            sorted(
                alumni["status"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    # -------------------------
    # Apply filters
    # -------------------------

    filtered = alumni.copy()

    if course_filter != "All":

        filtered = filtered[
            filtered["course"] == course_filter
        ]

    if industry_filter != "All":

        filtered = filtered[
            filtered["industry"] == industry_filter
        ]

    if status_filter != "All":

        filtered = filtered[
            filtered["status"] == status_filter
        ]

    st.write(
        f"### Showing {len(filtered)} alumni"
    )

    st.divider()

    # -------------------------
    # Alumni profiles
    # -------------------------

    for i in range(
        0,
        len(filtered),
        2
    ):

        cols = st.columns(2)

        for j, col in enumerate(cols):

            if i + j >= len(filtered):
                break

            person = filtered.iloc[i + j]

            with col:

                with st.container(border=True):

                    initials = "".join(
                        word[0].upper()
                        for word in person["name"].split()[:2]
                    )

                    st.subheader(
                        f"👤 {initials}  {person['name']}"
                    )

                    st.caption(
                        f"{person['course']} • "
                        f"Class of {person['graduation_year']}"
                    )

                    st.divider()

                    st.write(
                        f"🏢 **Company:** {person['company']}"
                    )

                    st.write(
                        f"💼 **Position:** {person['position']}"
                    )

                    st.write(
                        f"🏭 **Industry:** {person['industry']}"
                    )

                    st.write(
                        f"📍 **Location:** {person['location']}"
                    )

                    if person["status"] == "Working":

                        st.success(
                            "🟢 Working"
                        )

                    elif person["status"] == "Entrepreneur":

                        st.info(
                            "🚀 Entrepreneur"
                        )

                    elif person["status"] == "Higher Studies":

                        st.warning(
                            "🎓 Higher Studies"
                        )

                    else:

                        st.warning(
                            f"📊 {person['status']}"
                        )

                    if person["verified"] == "Verified":

                        st.success(
                            "✓ Verified Alumni"
                        )

                    else:

                        st.warning(
                            "⏳ Verification Pending"
                        )


# =========================================================
# SEARCH ALUMNI
# =========================================================

elif page == "🔍 Search Alumni":

    st.title("🔍 Search Alumni")

    st.caption(
        "Find alumni by name, company, role, industry or location."
    )

    st.divider()

    search = st.text_input(
        "Search Alumni",
        placeholder=(
            "Try Rahul, Google, Data Analyst, "
            "Bengaluru..."
        )
    )

    if search:

        mask = (

            alumni["name"].str.contains(
                search,
                case=False,
                na=False
            )

            |

            alumni["company"].str.contains(
                search,
                case=False,
                na=False
            )

            |

            alumni["position"].str.contains(
                search,
                case=False,
                na=False
            )

            |

            alumni["location"].str.contains(
                search,
                case=False,
                na=False
            )

            |

            alumni["industry"].str.contains(
                search,
                case=False,
                na=False
            )

            |

            alumni["course"].str.contains(
                search,
                case=False,
                na=False
            )
        )

        results = alumni[mask]

        st.divider()

        st.subheader(
            f"🔎 {len(results)} Results Found"
        )

        if len(results) > 0:

            for _, person in results.iterrows():

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )

                    with col1:

                        st.subheader(
                            f"👤 {person['name']}"
                        )

                        st.caption(
                            f"{person['course']} • "
                            f"Class of "
                            f"{person['graduation_year']}"
                        )

                    with col2:

                        st.write(
                            f"🏢 **{person['company']}**"
                        )

                        st.write(
                            f"💼 {person['position']}"
                        )

                    with col3:

                        st.write(
                            f"📍 {person['location']}"
                        )

                        st.write(
                            f"📊 {person['status']}"
                        )

        else:

            st.warning(
                "No matching alumni found."
            )

    else:

        st.info(
            "Start typing to search the alumni database."
        )


# =========================================================
# ALUMNI PROFILE
# =========================================================

elif page == "👤 Alumni Profile":

    st.title("👤 Alumni Profile")

    st.caption(
        "Explore all alumni profiles and their career information."
    )

    st.divider()

    # -----------------------------------------------------
    # Sort alumni
    # -----------------------------------------------------

    alumni = alumni.sort_values(
        "name"
    ).reset_index(drop=True)

    # -----------------------------------------------------
    # Session state
    # -----------------------------------------------------

    if "selected_alumni_id" not in st.session_state:

        st.session_state.selected_alumni_id = int(
            alumni.iloc[0]["id"]
        )

    # -----------------------------------------------------
    # Find current profile
    # -----------------------------------------------------

    selected_index = alumni.index[
        alumni["id"] ==
        st.session_state.selected_alumni_id
    ].tolist()

    if not selected_index:

        selected_index = [0]

        st.session_state.selected_alumni_id = int(
            alumni.iloc[0]["id"]
        )

    current_index = selected_index[0]

    # -----------------------------------------------------
    # Alumni selector
    # -----------------------------------------------------

    selected_name = st.selectbox(
        "🔍 Choose Alumni",
        alumni["name"].tolist(),
        index=current_index
    )

    person = alumni[
        alumni["name"] == selected_name
    ].iloc[0]

    st.session_state.selected_alumni_id = int(
        person["id"]
    )

    st.divider()

    # -----------------------------------------------------
    # Previous / Counter / Next
    # -----------------------------------------------------

    previous_col, count_col, next_col = st.columns(
        [1, 2, 1]
    )

    with previous_col:

        if st.button(
            "⬅ Previous",
            use_container_width=True
        ):

            new_index = (
                current_index - 1
            ) % len(alumni)

            st.session_state.selected_alumni_id = int(
                alumni.iloc[new_index]["id"]
            )

            st.rerun()

    with count_col:

        st.info(
            f"👥 Alumni {current_index + 1} "
            f"of {len(alumni)}"
        )

    with next_col:

        if st.button(
            "Next ➡",
            use_container_width=True
        ):

            new_index = (
                current_index + 1
            ) % len(alumni)

            st.session_state.selected_alumni_id = int(
                alumni.iloc[new_index]["id"]
            )

            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # Profile Header
    # -----------------------------------------------------

    col1, col2 = st.columns(
        [1, 4]
    )

    with col1:

        initials = "".join(
            word[0].upper()
            for word in person["name"].split()[:2]
        )

        st.title(
            f"👤 {initials}"
        )

    with col2:

        st.header(
            person["name"]
        )

        st.write(
            f"🎓 {person['course']} "
            f"• Class of {person['graduation_year']}"
        )

        if person["verified"] == "Verified":

            st.success(
                "✓ Verified Alumni"
            )

        else:

            st.warning(
                "⏳ Verification Pending"
            )

    st.divider()

    # -----------------------------------------------------
    # Career Information
    # -----------------------------------------------------

    st.subheader(
        "💼 Career Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🏢 Company",
            str(person["company"])
        )

    with col2:

        st.metric(
            "💼 Position",
            str(person["position"])
        )

    with col3:

        st.metric(
            "📍 Location",
            str(person["location"])
        )

    st.divider()

    # -----------------------------------------------------
    # Alumni Information
    # -----------------------------------------------------

    st.subheader(
        "📚 Alumni Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("📧 **Email**")

        st.info(
            str(person["email"])
        )

        st.write("🎓 **Course**")

        st.info(
            str(person["course"])
        )

        st.write("📅 **Graduation Year**")

        st.info(
            str(person["graduation_year"])
        )

    with col2:

        st.write("🏭 **Industry**")

        st.info(
            str(person["industry"])
        )

        st.write("📊 **Current Status**")

        if person["status"] == "Working":

            st.success(
                str(person["status"])
            )

        elif person["status"] == "Entrepreneur":

            st.info(
                str(person["status"])
            )

        else:

            st.warning(
                str(person["status"])
            )

        st.write("🌍 **Location**")

        st.info(
            str(person["location"])
        )

    st.divider()

    # -----------------------------------------------------
    # Career Timeline
    # -----------------------------------------------------

    st.subheader(
        "📈 Career Timeline"
    )

    st.success(
        f"🎓 {person['graduation_year']} — "
        f"Graduated in {person['course']}"
    )

    st.info(
        f"💼 Current — "
        f"{person['position']} at "
        f"{person['company']}"
    )

    st.info(
        f"📍 Currently based in "
        f"{person['location']}"
    )

    st.divider()

    # -----------------------------------------------------
    # Profile Summary
    # -----------------------------------------------------

    with st.expander(
        "📋 View Complete Profile"
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Alumni ID:** {person['id']}"
            )

            st.write(
                f"**Name:** {person['name']}"
            )

            st.write(
                f"**Email:** {person['email']}"
            )

            st.write(
                f"**Course:** {person['course']}"
            )

            st.write(
                f"**Graduation Year:** "
                f"{person['graduation_year']}"
            )

        with col2:

            st.write(
                f"**Company:** {person['company']}"
            )

            st.write(
                f"**Position:** {person['position']}"
            )

            st.write(
                f"**Industry:** {person['industry']}"
            )

            st.write(
                f"**Location:** {person['location']}"
            )

            st.write(
                f"**Status:** {person['status']}"
            )

            st.write(
                f"**Verification:** "
                f"{person['verified']}"
            )


# =========================================================
# CAREER HISTORY
# =========================================================

elif page == "📈 Career History":

    st.title("📈 Career Journey")

    st.caption(
        "Track the alumni journey from graduation to their current career."
    )

    st.divider()

    selected_name = st.selectbox(
        "👤 Select Alumni",
        alumni["name"].tolist()
    )

    person = alumni[
        alumni["name"] == selected_name
    ].iloc[0]

    st.subheader(
        person["name"]
    )

    st.caption(
        f"{person['course']} • "
        f"Class of {person['graduation_year']}"
    )

    st.divider()

    # Graduation

    st.success(
        f"🎓 {person['graduation_year']}"
    )

    st.write(
        f"**Graduated from {person['course']}**"
    )

    st.divider()

    # Career

    st.info(
        "💼 Career"
    )

    st.write(
        f"**Joined {person['company']}**"
    )

    st.write(
        f"Position: {person['position']}"
    )

    st.write(
        f"Industry: {person['industry']}"
    )

    st.divider()

    # Current

    st.success(
        "🚀 Present"
    )

    st.write(
        f"**{person['position']}**"
    )

    st.write(
        f"{person['company']} • "
        f"{person['location']}"
    )

    st.write(
        f"Current status: {person['status']}"
    )

    st.divider()

    # Career summary

    with st.expander(
        "📋 Career Summary"
    ):

        st.write(
            f"🎓 **Education:** "
            f"{person['course']}"
        )

        st.write(
            f"📅 **Graduation:** "
            f"{person['graduation_year']}"
        )

        st.write(
            f"🏢 **Company:** "
            f"{person['company']}"
        )

        st.write(
            f"💼 **Position:** "
            f"{person['position']}"
        )

        st.write(
            f"🏭 **Industry:** "
            f"{person['industry']}"
        )

        st.write(
            f"📍 **Location:** "
            f"{person['location']}"
        )

        st.write(
            f"📊 **Status:** "
            f"{person['status']}"
        )


# =========================================================
# UPDATE CAREER
# =========================================================

elif page == "✏️ Update Career":

    st.title("✏️ Update Career")

    st.caption(
        "Update an alumni profile directly in the database."
    )

    st.divider()

    selected_name = st.selectbox(
        "👤 Select Alumni",
        alumni["name"].tolist()
    )

    person = alumni[
        alumni["name"] == selected_name
    ].iloc[0]

    st.subheader(
        f"Updating: {person['name']}"
    )

    st.caption(
        f"{person['course']} • "
        f"Class of {person['graduation_year']}"
    )

    st.divider()

    # -----------------------------------------------------
    # Current information
    # -----------------------------------------------------

    st.info(
        f"Current company: {person['company']} | "
        f"Current position: {person['position']}"
    )

    # -----------------------------------------------------
    # Update fields
    # -----------------------------------------------------

    company = st.text_input(
        "🏢 Company",
        value=str(person["company"])
    )

    position = st.text_input(
        "💼 Position",
        value=str(person["position"])
    )

    industry = st.text_input(
        "🏭 Industry",
        value=str(person["industry"])
    )

    location = st.text_input(
        "📍 Location",
        value=str(person["location"])
    )

    status_options = [
        "Working",
        "Higher Studies",
        "Entrepreneur",
        "Looking for Job"
    ]

    current_status = (
        person["status"]
        if person["status"] in status_options
        else "Working"
    )

    status = st.selectbox(
        "📊 Status",
        status_options,
        index=status_options.index(
            current_status
        )
    )

    st.divider()

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    if st.button(
        "💾 Save Career Update",
        use_container_width=True
    ):

        update_alumni(
            person["id"],
            company,
            position,
            industry,
            location,
            status
        )

        st.success(
            f"✅ Successfully updated "
            f"{person['name']}!"
        )

        st.info(
            "The database has been updated. "
            "All dashboard pages will now use the new information."
        )

        st.rerun()