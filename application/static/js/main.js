document.addEventListener("DOMContentLoaded", () => {

    const getTonalityBtn = document.getElementsByClassName('getTonality')
    const getFactsBtn = document.getElementsByClassName('getFacts')

    query(getFactsBtn, urlDescriptions.facts)
    query(getTonalityBtn, urlDescriptions.tonality)

})


const urlDescriptions = {
    facts: {
        url: '/getFacts',
        id: 'fact_'
    },
    tonality: {
        url: '/getTonality',
        id: 'tonality_'
    }
}

function query(buttons, urlDescription) {
    for(const btn of buttons) {
        btn.addEventListener('click', async (event) => {
            const articleId = event.target.dataset.id
            const res = await fetch(`${urlDescription.url}/${articleId}`)
            const tonality = await res.json()
            console.log(tonality)
            const tonalityElement = document.getElementById(urlDescription.id + articleId)
            tonalityElement.innerText = JSON.stringify(tonality);
        })
    }

}