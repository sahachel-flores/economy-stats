import { useState, useRef, useEffect } from "react"

import SlideImage from "./SlidesImage";
import Captions from "./Captions";
import Control from "./Control";
import Dots from "./Dots";

const News = ({topic, items = demoItems, intervalMs = 2000}) => {
    const [isHovering, setIsHovering] = useState(false);
    const [index, setIndex] = useState(0);
    const touchStartX = useRef(0);
    const touchDeltaX = useRef(0);

    // Autoplay
    useEffect(() => {
        if (isHovering || items.length <= 1) return;
        const id = setInterval(() => setIndex((i) => (i + 1) % items.length), intervalMs);
        return () => clearInterval(id);
    }, [isHovering, items.length, intervalMs]);
    
    
    // Keyboard navigation
    useEffect(() => {
        const onKey = (e) => {
            if (e.key === "ArrowRight") next();
            if (e.key === "ArrowLeft") prev();
        };
        window.addEventListener("keydown", onKey);
        return () => window.removeEventListener("keydown", onKey);
    });

    const next = () => setIndex( (i) => (i + 1) % items.length);
    const prev = () => setIndex( (i) => (i - 1 + items.length) % items.length);

    const onTouchStart = (e) => {
        touchStartX.current = e.touches[0].clientX;
        touchDeltaX.current = 0;
    };

    const onTouchMove = (e) => {
        touchDeltaX.current = e.touches[0].clientX - touchStartX.current
    };
    
    const onTouchEnd = (e) => {
        const dx = e.touchDeltaX.current
        if (Math.abs(dx) > 50){
            if (dx < 0) next();
            else prev();
        }
    };

    const active = items[index]
    return(
        <section
            className="w-full max-w-5xl mx-auto m-6 select-none"
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
        >
             <div 
            className="relative overflow-hidden round-2xl shadow bg-white"
            onTouchStart={onTouchStart}
            onTouchMove={onTouchMove}
            onTouchEnd={onTouchEnd}
            >
                <h1 className="text-2xl font-bold text-center mb-4">{topic}</h1>
                <SlideImage active={active} placeholder={placeholder} />
                <Captions active={active} />
                <Control prev={prev} next={next} />
                <Dots index={index} items={items} setIndex={setIndex} />
            </div>
        </section>
    );
};



// Fallback image if an image fails to load
const placeholder =
"data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 225'>\
<rect width='400' height='225' fill='%23e5e7eb'/>\
<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='%239ca3af' font-family='Arial' font-size='16'>Image unavailable</text>\
</svg>";


// dummy items 
const demoItems = [
    {
        id: 1,
        topic: "us economy",
        title: "US Inflation Cools in October; Markets Rally",
        summary:
            "Headline CPI eased more than expected, boosting hopes for a soft landing as equities and bonds climbed across the board.",
        imageUrl:
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=1600&auto=format&fit=crop",
        href: "/news/1",
    },
    {
        id: 2,
        topic: "housing",
        title: "Jobless Claims Edge Lower, Labor Market Still Tight",
        summary:
            "Initial claims ticked down, suggesting ongoing resilience even as hiring plans moderate among large employers.",
        imageUrl:
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1600&auto=format&fit=crop",
        href: "/news/2",
    },
    {
        id: 3,
        topic: "stock",
        title: "Mortgage Rates Retreat, Sparking Refi Interest",
        summary:
            "Average 30-year fixed rates slipped for a third week, with lenders reporting a modest pickup in applications.",
        imageUrl:
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1600&auto=format&fit=crop",
        href: "/news/3",
    },
    {
        id: 4,
        topic: "labor",
        title: "Tech Earnings Beat Sends Nasdaq Higher",
        summary:
            "Mega-cap results surprised to the upside, with cloud and AI segments leading revenue growth.",
        imageUrl:
            "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1600&auto=format&fit=crop",
        href: "/news/4",
    },
    {
        id: 5,
        topic: "us economy",
        title: "Oil Slides on Supply Outlook, Strong Dollar",
        summary:
            "Crude prices fell as inventories rose and traders reassessed global demand into year-end.",
        imageUrl:
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=1600&auto=format&fit=crop",
        href: "/news/5",
    },
    ];


export default News;
