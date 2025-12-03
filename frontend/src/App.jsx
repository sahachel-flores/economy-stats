import Header from "./components/Header"
import NewsCarousel from "./components/NewsCarousel";
const App = () => {
  console.log("here");
  const topics = ['us economy', 'housing', 'stock', 'labor']
  
  
  return (
    <div>
      <Header />
      <h1>News</h1>
      {topics.map( (topic) => (
        <NewsCarousel topic={topic}/>
      ))}
    </div>
  );
};

export default App;
