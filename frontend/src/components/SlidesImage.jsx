const SlideImage = ({active, placeholder}) => {
    return(
        
        <>
            {/*slide images*/}
            <a href={active.href} className="block" aria-label={active.title}>
                <div className="w-full aspect-video bg-gray-100">
                    {/*Loading images */}
                    <img 
                        src={active.imageUrl}
                        alt={active.title}
                        className="w-full h-full object-cover"
                        loading="lazy"
                        onError={(e) => {e.currentTarget.src = placeholder}}
                    />

                </div>
            </a>
        </>
    );
}

export default SlideImage