const PORT = 8000
const axios = require('axios')
const cheerio = require('cheerio')
const express = require('express')
const app = express()


const url = 'https://en.wikipedia.org/wiki/Main_Page'
    const reply = []

function collect(name,$){

    $(name).each(function () { //<-- cannot be a function expression
        const urls = []
        const urlcont = []
        const article = $(this).find("div").find('p').text()

        const url = "https:"+ $(this).find('div').find('img').attr('src')
       $(this).find('div').find('p').find('a').each(function(){
        urlcont.push($(this).text())
        urls.push($(this).attr('href'))
        })
        reply.push({
            article,
            url,
            urlcont,
            urls
        })
    })
}
app.get('/', (req, res) => {
     axios(url)
        .then(response => {
            const html = response.data
            const $ = cheerio.load(html)
            collect('#mp-left',$)
            collect('#mp-right',$)
            collect('#mp-lower',$)
            res.json(reply)
        }).catch(err => console.log(err))

})


app.listen(PORT, () => console.log(`server running on PORT ${PORT} . . . . http://localhost:${PORT}`))