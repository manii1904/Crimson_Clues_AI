def load_css():

    return """
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Poppins:wght@300;400;500;600&display=swap');

*{
    font-family:'Poppins',sans-serif;
}

/* ===============================
BACKGROUND
=============================== */

.stApp{

    background:
    radial-gradient(circle at top,#1a1a1a 0%,#0f1015 40%,#07080b 100%);

    color:white;

}

/* ===============================
HIDE STREAMLIT
=============================== */

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

/* ===============================
HEADINGS
=============================== */

h1{

    font-family:'Cinzel',serif;

    color:#FFD700;

    text-shadow:
        0 0 10px #FFD700,
        0 0 20px #FFD700,
        0 0 40px rgba(255,215,0,.5);

    animation:glow 2s infinite alternate;

}
@keyframes glow{

    from{

        text-shadow:
        0 0 8px #FFD700;

    }

    to{

        text-shadow:
        0 0 25px #FFD700,
        0 0 45px #FFD700;

    }

}
h2{

    color:#FFD700;

    font-weight:700;

}

h3{

    color:white;

    font-weight:600;

}

h4{

    color:#dddddd;

}

/* ===============================
GLASS CARDS
=============================== */

div[data-testid="stVerticalBlock"] > div:hover{

    transform:
        translateY(-6px)
        scale(1.02);

    transition:.3s;

}

/* ===============================
BUTTONS
=============================== */

.stButton>button{

    width:100%;

    background:linear-gradient(135deg,#8B0000,#C1121F,#FF4D6D);

    color:white;

    font-size:18px;

    font-weight:700;

    border:none;

    border-radius:16px;

    padding:14px;

    transition:.35s;

    cursor:pointer;

    box-shadow:0 0 25px rgba(255,0,0,.35);

}

.stButton>button:hover{

    transform:
        scale(1.05);

    transition:.3s;

}


/* ===============================
TEXT INPUT
=============================== */

.stTextInput input,
textarea{

    background:#1B1E27 !important;

    color:white !important;

    border-radius:14px !important;

    border:1px solid rgba(255,215,0,.2) !important;

}

/* ===============================
SELECTBOX
=============================== */

.stSelectbox{

    border-radius:14px;

}

/* ===============================
SIDEBAR
=============================== */

section[data-testid="stSidebar"]{

    background:#11151D;

    border-right:1px solid rgba(255,215,0,.15);

}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{

    color:#FFD700;

}

/* ===============================
METRICS
=============================== */

div[data-testid="stMetric"]{

    background:rgba(255,255,255,.05);

    backdrop-filter:blur(12px);

    border-radius:18px;

    padding:20px;

    border:1px solid rgba(255,215,0,.18);

    box-shadow:0 6px 20px rgba(0,0,0,.35);

}

/* ===============================
CHAT
=============================== */

div[data-testid="stChatMessage"]{

    background:#1A1F2B;

    border-left:5px solid #FFD700;

    border-radius:15px;

    padding:15px;

}

/* ===============================
IMAGES
=============================== */

img{

    border-radius:18px;

    border:2px solid rgba(255,215,0,.18);

}

/* ===============================
SCROLLBAR
=============================== */

::-webkit-scrollbar{

    width:9px;

}

::-webkit-scrollbar-thumb{

    background:#FFD700;

    border-radius:10px;

}

/* ===============================
ANIMATION
=============================== */

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(20px);

    }

    to{

        opacity:1;

        transform:translateY(0px);

    }

}

.block-container{

    animation:fadeIn .7s ease;

}

/* ===============================
SUCCESS INFO WARNING
=============================== */

.stSuccess,
.stInfo,
.stWarning,
.stError{

    border-radius:16px;

}
/* ===============================
PAGE ANIMATION
=============================== */

@keyframes fadeUp{

    0%{
        opacity:0;
        transform:translateY(30px);
    }

    100%{
        opacity:1;
        transform:translateY(0px);
    }

}

.block-container{

    animation:fadeUp .8s ease;
}
</style>
"""