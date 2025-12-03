import ChevronLeft from "./ChevronLeft";
import ChevronRight from "./ChevronRight";
const Control = ({prev, next}) => {
    return (
        <>
            {/* Controls */}
            <button
                onClick={prev}
                aria-label="Previous slide"
                className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-white/80 hover:bg-white shadow p-2"
            >
                <ChevronLeft />
            </button>
            <button
                onClick={next}
                aria-label="Next slide"
                className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-white/80 hover:bg-white shadow p-2"
            >
                <ChevronRight />
            </button>
    </>
    )
}

export default Control;