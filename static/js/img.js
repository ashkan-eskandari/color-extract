const form = document.querySelector('form[name="color_extract"]');
const colorsSection = document.getElementById("colors_section")
const img = document.getElementById("file_url")
const table = document.getElementById("table")
const img_spinner = document.getElementById("img_spinner")
form.addEventListener('submit', evt => {
    evt.preventDefault();
    colorsSection.classList.add("d-none")
    table.innerHTML = ""
    img.src = ""
    img_spinner.classList.remove("d-none")
    fetch("/upload", {
        method: 'POST',
        body: new FormData(evt.target)
    }).then(resp => resp.json())
        .then(data => {
            let file_url = data.file_url
            let colors = data.colors
            let counts = data.counts
            img.src = file_url
            img_spinner.classList.add("d-none")
            colorsSection.classList.remove("d-none")
            for (let i = 0; i < colors.length; i++) {
                table.innerHTML += `<button type="button" class="btn btn-sm m-2" style="background-color: ${colors[i]}">
                               <span class="badge text-sm-secondary no-padding" id="hex" style="font-size: 10px">${colors[i]}</span>
                               <span class="badge text-sm-secondary" id="percent" style="font-size: 10px">${counts[i]} %</span>
                               </button>`;
            }

        }).catch(err => {
        console.error('Error:', err);
    })
        evt.target.reset();

})



