const Captions = ({active}) => {
    return (
        <>
        {/*Captions */}
        <div className="p-4">
            <a href={active.href} className="block">
                <h3 className="text-lg md:text-xl font-semibold text-gray-900 hover:underline">
                    {active.title}
                </h3>
            </a>
            <p className="mt-2 text-sm md:text-base text-gray-600 max-h-20 overflow-hidden">
                {active.summary}
            </p>
        </div>
        </>
    )
}

export default Captions;
