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

function transformToUl(arr, title) {
    let html = '';
    if (arr.length === 0) {
        html += `<p>Элементы ${title} не найдены</p>`
    } else {
        html += `<p>${title}</p>`
        html += '<ul>'
        if (typeof arr[Symbol.iterator] === 'function') {
            for (const elem of arr) {
                html += `<li>${JSON.stringify(elem).split(/\{|\}/g).join('')}</li>`
            }
        }
        else {
            html += JSON.stringify(arr)
        }
        html += '</ul>'
    }
    return html
}

function query(buttons, urlDescription) {
    for(const btn of buttons) {
        btn.addEventListener('click', async (event) => {
            const articleId = event.target.dataset.id
            const res = await fetch(`${urlDescription.url}/${articleId}`)
            const tonality = await res.json()
            console.log(tonality)
            const tonalityElement = document.getElementById(urlDescription.id + articleId)
            tonalityElement.innerHTML = Object.keys(tonality).reduce((acc, key) => acc + transformToUl(tonality[key], key), '')
        })
    }

}