const Dots = ({index, items, setIndex}) => {
    return (
        <>
        {/* Dots */}
        <div className="absolute bottom-3 left-0 right-0 flex justify-center gap-2">
            {items.map((_, i) => (
                <button
                    key={i}
                    onClick={() => setIndex(i)}
                    aria-label={`Go to slide ${i + 1}`}
                    className={
                        "h-2 w-2 rounded-full transition-all " +
                        (i === index ? "bg-blue-600 w-6" : "bg-gray-300 hover:bg-gray-400")
                    }
                />
            ))}
        </div>
    </>
    )
}

export default Dots;