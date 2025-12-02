import Header from "./components/Header"
import News from "./components/News";
const App = () => {
  console.log("here");
  const topics = ['us economy', 'housing', 'stock', 'labor']
  
  return (
    <div>
      <Header />
      <h1>News</h1>
      {topics.map( (topic) => (
        <News topic={topic}/>
      ))}
    </div>
  );
};

export default App;
