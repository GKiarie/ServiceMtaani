// code to search carousel for required part
const search = () => {
    const searchbox = document.getElementById("search-item").value.toUpperCase();
    const storeitems = document.getElementById("featuredParts");
    //get individual products
    const product = document.querySelectorAll(".featuredItem");
    const pname = document.querySelectorAll(".name");

    for(let i=0; i < pname.length; i++){
        let match = product[i].querySelectorAll('.name')[0];

        if (match) {
            let textvalue = match.textContent || match.innerHTML;

            if (textvalue.toUpperCase().indexOf(searchbox) > -1) {
                product[i].style.display = "";
            } else {
                product[i].style.display = "none";
            }

        }

        
    }
}