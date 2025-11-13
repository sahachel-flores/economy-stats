import Header from "./components/Header"
import News from "./components/News";
const App = () => {
  console.log("here");
  return (
    <div>
      <Header />
      <h1>News</h1>
      <News />
      <News />
      <News />
      <News />
    </div>
  );
};

export default App;
