
import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png", "webp", "gif", "svg"
}

PERSONAL_MESSAGE = """
Abbas,

Some people collect things.
Some people become part of the collection.

This little digital museum was made for you —
a small archive of the things that made your profile stand out.

81 gifts.
A rare Diamond.
Plush Pepe.
And a story worth keeping.

This is your collection.
This is your archive.
This is ABBAS.
"""


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_images():
    images = []

    for filename in os.listdir(ASSETS_DIR):
        if allowed_file(filename):
            images.append(filename)

    return sorted(images)


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ABBAS — Digital Museum</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    background:#050505;
    color:#fff;
    font-family:Arial,Helvetica,sans-serif;
    overflow-x:hidden;
}

::selection{
    background:#d71920;
    color:white;
}

body:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:9999;
    opacity:.025;
    background-image:
        repeating-radial-gradient(
            circle at 0 0,
            #fff 0,
            transparent 1px,
            transparent 4px
        );
}

.ambient{
    position:fixed;
    width:700px;
    height:700px;
    border-radius:50%;
    background:rgba(180,0,0,.10);
    filter:blur(110px);
    top:-350px;
    left:-300px;
    pointer-events:none;
    z-index:-1;
}

.ambient.two{
    top:auto;
    left:auto;
    right:-350px;
    bottom:-350px;
}

/* INTRO */

#intro{
    position:fixed;
    inset:0;
    background:#000;
    z-index:10000;
    display:flex;
    align-items:center;
    justify-content:center;
    transition:opacity 1.3s ease,visibility 1.3s ease;
}

#intro.hide{
    opacity:0;
    visibility:hidden;
}

.intro-content{
    text-align:center;
}

.intro-small{
    font-size:11px;
    letter-spacing:8px;
    color:#777;
    margin-bottom:28px;
    opacity:0;
    animation:smallIn 1.5s forwards .5s;
}

.intro-name{
    font-size:clamp(60px,13vw,180px);
    font-weight:900;
    letter-spacing:15px;
    color:transparent;
    -webkit-text-stroke:1px rgba(255,255,255,.25);
    position:relative;
    opacity:0;
    animation:nameIn 2s forwards 1.2s;
}

.intro-name:after{
    content:"ABBAS";
    position:absolute;
    left:0;
    top:0;
    width:0;
    overflow:hidden;
    white-space:nowrap;
    color:#fff;
    animation:revealName 2s forwards 1.8s;
}

.intro-line{
    width:0;
    height:1px;
    background:#d71920;
    margin:35px auto 0;
    animation:lineIn 1.5s forwards 2.6s;
}

@keyframes smallIn{
    to{opacity:1;transform:translateY(-5px);}
}

@keyframes nameIn{
    to{opacity:1;}
}

@keyframes revealName{
    to{width:100%;}
}

@keyframes lineIn{
    to{width:180px;}
}

/* NAV */

nav{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:80px;
    padding:0 6vw;
    display:flex;
    align-items:center;
    justify-content:space-between;
    z-index:500;
    background:linear-gradient(to bottom,rgba(0,0,0,.9),transparent);
}

.logo{
    font-size:18px;
    font-weight:900;
    letter-spacing:4px;
}

.logo span{
    color:#d71920;
}

.nav-links{
    display:flex;
    gap:28px;
}

.nav-links a{
    color:#888;
    text-decoration:none;
    font-size:10px;
    letter-spacing:2px;
    text-transform:uppercase;
    transition:.3s;
}

.nav-links a:hover{
    color:white;
}

/* HERO */

.hero{
    min-height:100vh;
    display:flex;
    align-items:center;
    padding:120px 8vw 80px;
    background:
        radial-gradient(circle at center,rgba(150,0,0,.12),transparent 45%);
}

.hero-inner{
    max-width:1200px;
    width:100%;
}

.hero-tag{
    color:#d71920;
    font-size:10px;
    letter-spacing:6px;
    margin-bottom:25px;
}

.hero h1{
    font-size:clamp(65px,12vw,170px);
    line-height:.85;
    font-weight:900;
    letter-spacing:-5px;
}

.hero h1 span{
    color:transparent;
    -webkit-text-stroke:1px #555;
}

.hero-description{
    max-width:580px;
    color:#888;
    line-height:1.8;
    margin-top:45px;
    font-size:15px;
}

.hero-bottom{
    margin-top:70px;
    display:flex;
    gap:60px;
    flex-wrap:wrap;
}

.hero-stat{
    border-left:1px solid #333;
    padding-left:18px;
}

.hero-stat strong{
    display:block;
    font-size:28px;
}

.hero-stat small{
    color:#666;
    letter-spacing:2px;
    font-size:9px;
}

/* SECTIONS */

section{
    padding:130px 8vw;
    position:relative;
}

.section-title{
    margin-bottom:65px;
}

.section-label{
    color:#d71920;
    font-size:10px;
    letter-spacing:5px;
    margin-bottom:15px;
}

.section-title h2{
    font-size:clamp(38px,6vw,80px);
    letter-spacing:-2px;
}

/* ABOUT */

.about-grid{
    max-width:1200px;
    margin:auto;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:80px;
}

.about-text{
    color:#888;
    line-height:2;
    font-size:15px;
}

.about-text strong{
    color:white;
}

.about-card{
    padding:45px;
    border:1px solid #202020;
    background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.005));
}

.about-card h3{
    font-size:30px;
    margin-bottom:25px;
}

.about-card p{
    color:#777;
    line-height:1.9;
}

/* DIAMOND */

.diamond-section{
    background:radial-gradient(circle at 80% 50%,rgba(120,0,0,.15),transparent 40%);
}

.diamond-box{
    max-width:1250px;
    margin:auto;
    display:grid;
    grid-template-columns:1fr 1fr;
    min-height:600px;
    border:1px solid #252525;
    background:#090909;
    overflow:hidden;
}

.diamond-visual{
    min-height:600px;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    background:radial-gradient(circle,rgba(255,0,0,.12),transparent 50%);
}

.diamond-glow{
    position:absolute;
    width:300px;
    height:300px;
    border-radius:50%;
    background:rgba(255,0,0,.08);
    filter:blur(80px);
    animation:pulse 4s infinite alternate;
}

@keyframes pulse{
    from{transform:scale(.8);opacity:.4;}
    to{transform:scale(1.2);opacity:.8;}
}

.diamond{
    width:190px;
    height:190px;
    transform:rotate(45deg);
    background:linear-gradient(135deg,#fff,#9b9b9b 35%,#333 60%,#fff);
    box-shadow:0 0 30px rgba(255,255,255,.35),0 0 100px rgba(255,0,0,.15);
    animation:diamondFloat 4s ease-in-out infinite;
}

@keyframes diamondFloat{
    0%,100%{transform:rotate(45deg) translateY(0);}
    50%{transform:rotate(45deg) translateY(-18px);}
}

.diamond-info{
    padding:80px 65px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.diamond-number{
    color:#555;
    font-size:10px;
    letter-spacing:4px;
    margin-bottom:25px;
}

.diamond-info h2{
    font-size:clamp(45px,6vw,80px);
    line-height:.9;
    margin-bottom:30px;
}

.diamond-info h2 span{
    color:#d71920;
}

.diamond-info h3{
    font-size:17px;
    letter-spacing:2px;
    margin-bottom:20px;
}

.diamond-info p{
    color:#777;
    line-height:1.9;
    max-width:500px;
}

.diamond-signature{
    margin-top:40px;
    padding-top:25px;
    border-top:1px solid #222;
    color:#aaa;
    font-size:12px;
    letter-spacing:2px;
}

/* PEPE */

.pepe-box{
    max-width:1250px;
    margin:auto;
    display:grid;
    grid-template-columns:1fr 1fr;
    min-height:550px;
    border:1px solid #222;
    background:linear-gradient(135deg,#080808,#101010);
}

.pepe-visual{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:550px;
}

.pepe-circle{
    width:300px;
    height:300px;
    border-radius:50%;
    border:1px solid #333;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 0 80px rgba(0,0,0,.8);
    position:relative;
}

.pepe-circle:after{
    content:"PEPE";
    color:#333;
    font-size:60px;
    font-weight:900;
    letter-spacing:-4px;
}

.pepe-info{
    padding:75px 65px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.pepe-label{
    color:#777;
    font-size:10px;
    letter-spacing:4px;
    margin-bottom:20px;
}

.pepe-info h2{
    font-size:clamp(40px,5vw,70px);
    line-height:.95;
    margin-bottom:30px;
}

.pepe-info h2 span{
    color:#777;
}

.pepe-info p{
    color:#777;
    line-height:1.9;
}

.holder-badge{
    display:inline-block;
    margin-top:35px;
    padding:12px 18px;
    border:1px solid #333;
    color:#ddd;
    font-size:10px;
    letter-spacing:3px;
    width:max-content;
}

/* GALLERY */

.gallery{
    max-width:1300px;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:20px;
}

.gallery-card{
    background:#0b0b0b;
    border:1px solid #202020;
    overflow:hidden;
    cursor:pointer;
    transition:.4s;
}

.gallery-card:hover{
    transform:translateY(-8px);
    border-color:#555;
}

.gallery-card img{
    width:100%;
    height:280px;
    object-fit:cover;
    display:block;
    transition:.6s;
}

.gallery-card:hover img{
    transform:scale(1.04);
}

.gallery-info{
    padding:20px;
}

.gallery-info small{
    color:#555;
    letter-spacing:2px;
    font-size:9px;
}

.gallery-info h3{
    margin-top:8px;
    font-size:16px;
}

/* TIMELINE */

.timeline{
    max-width:1000px;
    margin:auto;
    position:relative;
}

.timeline:before{
    content:"";
    position:absolute;
    left:50%;
    top:0;
    bottom:0;
    width:1px;
    background:#222;
}

.timeline-item{
    width:50%;
    padding:30px 50px;
    position:relative;
}

.timeline-item:nth-child(even){
    margin-left:50%;
}

.timeline-item:before{
    content:"";
    width:9px;
    height:9px;
    border-radius:50%;
    background:#d71920;
    position:absolute;
    top:38px;
    right:-5px;
}

.timeline-item:nth-child(even):before{
    left:-5px;
}

.timeline-year{
    color:#d71920;
    font-size:11px;
    letter-spacing:3px;
    margin-bottom:12px;
}

.timeline-item h3{
    margin-bottom:10px;
}

.timeline-item p{
    color:#666;
    line-height:1.8;
    font-size:14px;
}

/* TELEGRAM */

.telegram-box{
    max-width:1100px;
    margin:auto;
    border:1px solid #242424;
    padding:70px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:50px;
    background:radial-gradient(circle at 90% 50%,rgba(215,25,32,.12),transparent 40%);
}

.telegram-box h2{
    font-size:45px;
}

.telegram-box p{
    color:#777;
    margin-top:15px;
    line-height:1.8;
}

.telegram-button{
    display:inline-block;
    text-decoration:none;
    color:white;
    border:1px solid #444;
    padding:17px 30px;
    font-size:11px;
    letter-spacing:3px;
    transition:.3s;
}

.telegram-button:hover{
    background:#d71920;
    border-color:#d71920;
}

/* FINAL */

.final{
    min-height:80vh;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    background:radial-gradient(circle,rgba(150,0,0,.12),transparent 50%);
}

.final-content{
    max-width:900px;
}

.final-label{
    color:#d71920;
    font-size:10px;
    letter-spacing:5px;
    margin-bottom:30px;
}

.final h2{
    font-size:clamp(45px,8vw,100px);
    line-height:.95;
    margin-bottom:40px;
}

.final p{
    white-space:pre-line;
    color:#777;
    line-height:2;
    font-size:15px;
}

/* FOOTER */

footer{
    padding:50px 8vw;
    border-top:1px solid #151515;
    display:flex;
    justify-content:space-between;
    color:#444;
    font-size:10px;
    letter-spacing:2px;
}

/* LIGHTBOX */

#lightbox{
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.94);
    z-index:9000;
    display:none;
    align-items:center;
    justify-content:center;
    padding:30px;
}

#lightbox img{
    max-width:90vw;
    max-height:90vh;
    object-fit:contain;
}

.close{
    position:absolute;
    top:25px;
    right:35px;
    color:white;
    font-size:35px;
    cursor:pointer;
}

/* REVEAL */

.reveal{
    opacity:0;
    transform:translateY(35px);
    transition:opacity 1s ease,transform 1s ease;
}

.reveal.visible{
    opacity:1;
    transform:translateY(0);
}

/* MOBILE */

@media(max-width:850px){

    .nav-links{
        display:none;
    }

    section{
        padding:90px 6vw;
    }

    .about-grid,
    .diamond-box,
    .pepe-box{
        grid-template-columns:1fr;
    }

    .diamond-visual,
    .pepe-visual{
        min-height:400px;
    }

    .diamond-info,
    .pepe-info{
        padding:55px 35px;
    }

    .timeline:before{
        left:10px;
    }

    .timeline-item,
    .timeline-item:nth-child(even){
        width:100%;
        margin-left:0;
        padding-left:40px;
        padding-right:10px;
    }

    .timeline-item:before,
    .timeline-item:nth-child(even):before{
        left:6px;
        right:auto;
    }

    .telegram-box{
        padding:45px 30px;
        flex-direction:column;
        align-items:flex-start;
    }

    footer{
        flex-direction:column;
        gap:15px;
    }
}

</style>
</head>

<body>

<div class="ambient"></div>
<div class="ambient two"></div>

<!-- INTRO -->

<div id="intro">

    <div class="intro-content">

        <div class="intro-small">
            A DIGITAL GIFT
        </div>

        <div class="intro-name">
            ABBAS
        </div>

        <div class="intro-line"></div>

    </div>

</div>

<!-- NAV -->

<nav>

    <div class="logo">
        A<span>.</span>
    </div>

    <div class="nav-links">
        <a href="#about">About</a>
        <a href="#diamond">Diamond</a>
        <a href="#pepe">Pepe</a>
        <a href="#collection">Collection</a>
        <a href="#timeline">Journey</a>
        <a href="#telegram">Telegram</a>
        <a href="/upload">Upload</a>
    </div>

</nav>

<!-- HERO -->

<section class="hero">

    <div class="hero-inner">

        <div class="hero-tag">
            DIGITAL MUSEUM / PERSONAL ARCHIVE
        </div>

        <h1>
            ABBAS
            <br>
            <span>ARCHIVE.</span>
        </h1>

        <p class="hero-description">
            A digital archive created around the profile,
            collection and story of Abbas — built as a
            cinematic personal gift.
        </p>

        <div class="hero-bottom">

            <div class="hero-stat">
                <strong>81</strong>
                <small>GIFTS</small>
            </div>

            <div class="hero-stat">
                <strong>31.4K</strong>
                <small>SUBSCRIBERS</small>
            </div>

            <div class="hero-stat">
                <strong>2013</strong>
                <small>ESTABLISHED</small>
            </div>

        </div>

    </div>

</section>

<!-- ABOUT -->

<section id="about">

    <div class="section-title reveal">

        <div class="section-label">
            01 / ABOUT
        </div>

        <h2>
            THE PERSON
        </h2>

    </div>

    <div class="about-grid">

        <div class="about-text reveal">

            <p>
                Abbas is presented here through a collection
                of digital moments, Telegram collectibles,
                milestones and memories.
            </p>

            <br>

            <p>
                The idea behind this website is simple:
                turn a profile into something that feels
                more like a <strong>museum</strong> than
                a normal webpage.
            </p>

        </div>

        <div class="about-card reveal">

            <h3>
                SOCIAL GROWTH
            </h3>

            <p>
                Social Growth Manager — Ads, Reach &
                Audience Strategy.
            </p>

            <br>

            <p>
                Est. 2013
            </p>

        </div>

    </div>

</section>

<!-- DIAMOND -->

<section id="diamond" class="diamond-section">

    <div class="section-title reveal">

        <div class="section-label">
            02 / THE RARE PIECE
        </div>

        <h2>
            THE DIAMOND
        </h2>

    </div>

    <div class="diamond-box reveal">

        <div class="diamond-visual">

            <div class="diamond-glow"></div>

            <div class="diamond"></div>

        </div>

        <div class="diamond-info">

            <div class="diamond-number">
                SPECIAL COLLECTION / 001
            </div>

            <h2>
                THE
                <span>DIAMOND</span>
            </h2>

            <h3>
                A GIFT FROM PAVEL DUROV
            </h3>

            <p>
                One of the most distinctive pieces in
                Abbas's digital collection — a Diamond
                gifted by Pavel Durov.
            </p>

            <div class="diamond-signature">
                ABBAS × DUROV
            </div>

        </div>

    </div>

</section>

<!-- PEPE -->

<section id="pepe">

    <div class="section-title reveal">

        <div class="section-label">
            03 / COLLECTIBLE
        </div>

        <h2>
            PLUSH PEPE
        </h2>

    </div>

    <div class="pepe-box reveal">

        <div class="pepe-visual">
            <div class="pepe-circle"></div>
        </div>

        <div class="pepe-info">

            <div class="pepe-label">
                COLLECTIBLE / PEPE
            </div>

            <h2>
                ONE OF THE
                <span>HOLDERS.</span>
            </h2>

            <p>
                حالا وی یکی از هولدرهای Plush Pepe هستش.
                <br><br>
                A standout collectible from the collection,
                preserved here as one of the defining pieces
                of the archive.
            </p>

            <div class="holder-badge">
                PLUSH PEPE HOLDER
            </div>

        </div>

    </div>

</section>

<!-- COLLECTION -->

<section id="collection">

    <div class="section-title reveal">

        <div class="section-label">
            04 / THE COLLECTION
        </div>

        <h2>
            THE ARCHIVE
        </h2>

    </div>

    <div class="gallery">

        {% if images %}

            {% for image in images %}

            <div
                class="gallery-card reveal"
                onclick="openLightbox('/assets/{{ image }}')"
            >

                <img
                    src="/assets/{{ image }}"
                    alt="Abbas Collection"
                >

                <div class="gallery-info">

                    <small>
                        COLLECTION ITEM
                    </small>

                    <h3>
                        ABBAS / DIGITAL GIFT
                    </h3>

                </div>

            </div>

            {% endfor %}

        {% else %}

            <div style="
                grid-column:1/-1;
                text-align:center;
                padding:80px 20px;
                border:1px dashed #333;
                color:#555;
            ">

                No collection images uploaded yet.

                <br><br>

                <a
                    href="/upload"
                    style="color:#d71920;text-decoration:none;"
                >
                    UPLOAD COLLECTION
                </a>

            </div>

        {% endif %}

    </div>

</section>

<!-- TIMELINE -->

<section id="timeline">

    <div class="section-title reveal">

        <div class="section-label">
            05 / JOURNEY
        </div>

        <h2>
            TIMELINE
        </h2>

    </div>

    <div class="timeline">

        <div class="timeline-item reveal">

            <div class="timeline-year">
                2013
            </div>

            <h3>
                ESTABLISHED
            </h3>

            <p>
                The profile's public bio references
                2013 as the starting point.
            </p>

        </div>

        <div class="timeline-item reveal">

            <div class="timeline-year">
                TELEGRAM
            </div>

            <h3>
                THE COLLECTION
            </h3>

            <p>
                Telegram became a space for building
                an identity, audience and collection
                of digital collectibles.
            </p>

        </div>

        <div class="timeline-item reveal">

            <div class="timeline-year">
                TODAY
            </div>

            <h3>
                THE ARCHIVE
            </h3>

            <p>
                81 gifts and a growing collection —
                now preserved inside this digital museum.
            </p>

        </div>

    </div>

</section>

<!-- TELEGRAM -->

<section id="telegram">

    <div class="section-title reveal">

        <div class="section-label">
            06 / TELEGRAM
        </div>

        <h2>
            THE PROFILE
        </h2>

    </div>

    <div class="telegram-box reveal">

        <div>

            <h2>
                @abbas
            </h2>

            <p>
                A digital identity, collection and
                audience built around Telegram.
            </p>

        </div>

        <a
            class="telegram-button"
            href="https://t.me/abbas"
            target="_blank"
        >
            OPEN TELEGRAM
        </a>

    </div>

</section>

<!-- FINAL -->

<section class="final">

    <div class="final-content reveal">

        <div class="final-label">
            FINAL PAGE
        </div>

        <h2>
            THIS IS
            <br>
            ABBAS.
        </h2>

        <p>
            {{ message }}
        </p>

    </div>

</section>

<footer>

    <div>
        ABBAS DIGITAL MUSEUM
    </div>

    <div>
        CREATED AS A DIGITAL GIFT
    </div>

</footer>

<!-- LIGHTBOX -->

<div id="lightbox">

    <div class="close" onclick="closeLightbox()">
        ×
    </div>

    <img id="lightboxImage">

</div>

<script>

setTimeout(function(){

    document
        .getElementById("intro")
        .classList.add("hide");

},4300);


const observer = new IntersectionObserver(
    function(entries){

        entries.forEach(function(entry){

            if(entry.isIntersecting){
                entry.target.classList.add("visible");
            }

        });

    },
    {threshold:.12}
);


document
    .querySelectorAll(".reveal")
    .forEach(function(el){

        observer.observe(el);

    });


function openLightbox(src){

    document
        .getElementById("lightboxImage")
        .src = src;

    document
        .getElementById("lightbox")
        .style.display = "flex";
}


function closeLightbox(){

    document
        .getElementById("lightbox")
        .style.display = "none";
}


document
    .getElementById("lightbox")
    .addEventListener("click",function(e){

        if(e.target === this){
            closeLightbox();
        }

    });

</script>

</body>
</html>
"""


# ============================================================
# UPLOAD PAGE
# ============================================================

UPLOAD_HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,initial-scale=1.0">

<title>Upload — Abbas Digital Museum</title>

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    min-height:100vh;
    background:#050505;
    color:white;
    font-family:Arial,Helvetica,sans-serif;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:30px;
}

.box{
    width:100%;
    max-width:850px;
    padding:70px;
    border:1px solid #252525;
    background:
        radial-gradient(
            circle at top right,
            rgba(180,0,0,.12),
            transparent 45%
        );
    text-align:center;
}

.logo{
    color:#d71920;
    font-size:11px;
    letter-spacing:6px;
    margin-bottom:25px;
}

h1{
    font-size:clamp(45px,8vw,90px);
    margin:0 0 20px;
}

p{
    color:#777;
    line-height:1.8;
}

input[type=file]{
    display:none;
}

.choose{
    display:inline-block;
    margin-top:30px;
    padding:18px 30px;
    background:#d71920;
    cursor:pointer;
    font-size:11px;
    letter-spacing:3px;
}

.submit{
    display:block;
    margin:25px auto 0;
    padding:16px 35px;
    background:transparent;
    color:white;
    border:1px solid #444;
    cursor:pointer;
    font-size:11px;
    letter-spacing:3px;
}

#files{
    margin-top:25px;
    color:#666;
    font-size:12px;
    line-height:2;
}

.back{
    display:inline-block;
    margin-top:35px;
    color:#555;
    text-decoration:none;
    font-size:10px;
    letter-spacing:2px;
}

</style>

</head>

<body>

<div class="box">

    <div class="logo">
        ABBAS DIGITAL MUSEUM
    </div>

    <h1>
        UPLOAD
    </h1>

    <p>
        عکس‌های کالکشن را انتخاب کن تا مستقیماً
        وارد گالری سایت شوند.
        <br>
        امکان انتخاب چند عکس همزمان وجود دارد.
    </p>

    <form
        method="POST"
        action="/upload"
        enctype="multipart/form-data"
    >

        <label class="choose">

            SELECT IMAGES

            <input
                id="imageInput"
                type="file"
                name="images"
                multiple
                accept=".jpg,.jpeg,.png,.webp,.gif,.svg"
            >

        </label>

        <div id="files">
            No files selected.
        </div>

        <button
            class="submit"
            type="submit"
        >
            ADD TO COLLECTION
        </button>

    </form>

    <a class="back" href="/">
        ← BACK TO MUSEUM
    </a>

</div>

<script>

const input =
    document.getElementById("imageInput");

const files =
    document.getElementById("files");

input.addEventListener("change",function(){

    if(!input.files.length){

        files.innerText =
            "No files selected.";

        return;
    }

    let text="";

    for(const file of input.files){

        text += "• " + file.name + "<br>";

    }

    files.innerHTML=text;

});

</script>

</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML,
        images=get_images(),
        message=PERSONAL_MESSAGE
    )


@app.route("/assets/<path:filename>")
def assets(filename):

    return send_from_directory(
        ASSETS_DIR,
        filename
    )


@app.route("/upload", methods=["GET","POST"])
def upload():

    if request.method == "POST":

        uploaded_files = request.files.getlist("images")

        for file in uploaded_files:

            if not file:
                continue

            filename = secure_filename(file.filename)

            if not filename:
                continue

            if allowed_file(filename):

                base, ext = os.path.splitext(filename)

                final_name = filename
                counter = 1

                while os.path.exists(
                    os.path.join(
                        ASSETS_DIR,
                        final_name
                    )
                ):

                    final_name = (
                        f"{base}_{counter}{ext}"
                    )

                    counter += 1

                file.save(
                    os.path.join(
                        ASSETS_DIR,
                        final_name
                    )
                )

        return redirect(url_for("home"))

    return render_template_string(UPLOAD_HTML)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000)),
        debug=False
    )
