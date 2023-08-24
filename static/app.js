const BASE_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", function () {

    function generateListMarkup(cupcake) {
        return `<div data-cupcake-id=${cupcake.id}>
        <li> ${cupcake.flavor}
        <br>
        <small>Size: ${cupcake.size} | Rating: ${cupcake.rating}/10 </small>
        <br>
        <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake" class="img-thumbnail">
        <button class="delete-cupcake" data-id="${cupcake.id}">X</button>
        </li>
        </div>`
    };



    async function showCupcakes() {
        const response = await axios.get(`${BASE_URL}/cupcakes`);
        const cupcakesList = document.getElementById('cupcakes-list');
        for (let cupcakeData of response.data.cupcakes) {
            const newCupcake = generateListMarkup(cupcakeData);
            const cupcakeDiv = document.createElement('div');
            cupcakeDiv.innerHTML = newCupcake;
            cupcakesList.appendChild(cupcakeDiv);
        };
        return cupcakesList;
    };

    $("#new-cupcake-form").on("submit", async function (evt) {
        evt.preventDefault();

        let flavor = $("#form-flavor").val();
        let rating = $("#form-rating").val();
        let size = $("#form-size").val();
        let image = $("#form-image").val();

        const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
            flavor,
            rating,
            size,
            image
        });

        let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
        $("#cupcakes-list").append(newCupcake);
        $("#new-cupcake-form").trigger("reset");
    });

    showCupcakes();

    $("#cupcakes-list").on("click", ".delete-cupcake", deleteCupcake);

    async function deleteCupcake() {
        const id = $(this).data('id')
        await axios.delete(`${BASE_URL}/cupcakes/${id}`)
        $(this).parent().remove()
    }

})