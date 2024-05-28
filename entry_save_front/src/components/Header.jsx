export default function Example() {
  return (
    <>
      <div className="h-[25vh] md:h-[30vh] lg:h-[50vh] relative isolate overflow-hidden bg-gray-900">
        <img
          src="https://images.unsplash.com/photo-1577985051167-0d49eec21977?q=80&w=2089&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt=""
          className="brightness-50 saturate-50 absolute inset-0 -z-10 h-full w-full object-cover object-right md:object-center"
        />
        {/* Codigo para el degradao */}
        <div className="absolute w-full bottom-1/3 left-0 line-block px-8 lg:px-12">
          <div className="mx-auto pt-20 lg:mx-0 ">
            <h1 className="text-white font-bold text-4xl sm:text-6xl md:text-7xl lg:text-8xl text-center"> Save Library</h1>
            <p className="text-sm sm:text-md md:text-xl lg:text-2xl text-white text-center"> Una libreria organizada y segura. </p>
          </div>
        </div>
      </div>
    </>
  )
}


