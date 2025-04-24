import "./plan_page.css";
import { useState, useEffect } from 'react';

const PlanPage = () => {
  const [data, setData] = useState([]);
  const [elements, setElements] = useState([]); // Now using state
  const loca = "Manali"; // Keeping your original constant

  useEffect(() => {
    fetch("./csvjson.json")
      .then((response) => response.json())
      .then((jsonData) => {
        setData(jsonData);
        
        // Temporary array for processing
        const tempElements = [];
        
        // Process matching places
        jsonData.forEach((entry) => {
          if (entry.City === loca) {
            const [nplace1, nplace2] = `${entry.Place} ~ ${entry.Place_desc}`.split("~");
            tempElements.push(
              <div key={tempElements.length} className="data-box">
                <h2>{nplace1.trim()}</h2>
                <p>{nplace2.trim()}</p>
                <input
                  type="checkbox"
                  className="check"
                  id={`checkbox${tempElements.length + 1}`}
                />
              </div>
            );
          }
        });

        setElements(tempElements); // Update state once
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [loca]); // Dependency array remains

  return <div className="data-container">{elements}</div>;
};

export default PlanPage;
