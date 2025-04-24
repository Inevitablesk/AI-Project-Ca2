import "./plan_page.css";
import { useState, useEffect } from 'react';

const PlanPage = () => {
  const [planData, setPlanData] = useState(null);
  const [userInputs, setUserInputs] = useState({
    places: '',
    days: 3,
    people: 2,
    startDate: ''
  });

  // Search form component
  const SearchForm = () => (
    <div className="search-box">
      <input 
        type="text" 
        placeholder="Places to visit (comma separated)"
        onChange={(e) => setUserInputs({...userInputs, places: e.target.value})}
      />
      <input
        type="number"
        placeholder="Number of days"
        value={userInputs.days}
        onChange={(e) => setUserInputs({...userInputs, days: e.target.value})}
      />
      <button onClick={handleGeneratePlan}>Generate Plan</button>
    </div>
  );

  // Plan display component
  const PlanDisplay = () => (
    <div className="data-container">
      {planData?.Days?.map((day, index) => (
        <div key={index} className="data-box">
          <h2>Day {index + 1}</h2>
          <p>{day.activities}</p>
          <div className="hotel-section">
            <h3>Hotels</h3>
            {planData.Hotels?.map((hotel, i) => (
              <div key={i} className="hotel-card">
                <span>{hotel.name}</span>
                <span>Price: ₹{hotel.price}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  // Handle plan generation
  const handleGeneratePlan = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate-plan', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userInputs)
      });
      
      const data = await response.json();
      setPlanData(data);
      
    } catch (error) {
      console.error("Planning failed:", error);
    }
  };

  return (
    <div className="plan-page-container">
      <SearchForm />
      {planData ? <PlanDisplay /> : (
        <div className="default-message">
          <p>Enter your travel details to generate a personalized plan!</p>
        </div>
      )}
    </div>
  );
};

export default PlanPage;
