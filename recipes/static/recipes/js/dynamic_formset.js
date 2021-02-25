/* Core logic from:
    https://engineertodeveloper.com/dynamic-formsets-with-django/
*/

const ingredientForm = document.getElementsByClassName("ingredient-form");
const recipeForm = document.querySelector("#recipe-form");
const addIngredientFormBtn = document.querySelector("#add-ingredient-form");
const submitFormBtn = document.querySelector('#submit-form');
const totalForms = document.querySelector("#id_ingredients-TOTAL_FORMS");

let formCount = ingredientForm.length - 1;

function updateForms() {
    let count = 0;
    for (let form of ingredientForm) {
        const formRegex = RegExp(`form-(\\d){1}-`, 'g');
        form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`)
    }
}

addIngredientFormBtn.addEventListener("click", function (event) {
    event.preventDefault();

    const newIngredientForm = ingredientForm[0].cloneNode(true);
    const formRegex = RegExp(`form-(\\d){1}-`, 'g');

    formCount++;

    newIngredientForm.innerHTML = newIngredientForm.innerHTML.replace(formRegex, `form-${formCount}-`);
    recipeForm.insertBefore(newIngredientForm, submitFormBtn);
    totalForms.setAttribute('value', `${formCount + 1}`);
});

recipeForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-ingredient-form")) {
        event.preventDefault();
        event.target.parentElement.remove();
        formCount--;
        updateForms();
        totalForms.setAttribute('value', `${formCount + 1}`);
    }
});