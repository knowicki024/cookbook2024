import React, { useState, useEffect } from 'react';

function Home() {
    const[recipes, setRecipes] = useState([]);

    useEffect(() => {
        fetch('/recipes')
            .then((r) => r.json())
            .then((fetchedRecipes) => setRecipes(fetchedRecipes))
            .catch((error) => console.error('Error fetching recipes'));
    },[]);


    return (
        <div>
            <Recipes recipes={recipes}/>
        </div>
    );
}

export default Home;