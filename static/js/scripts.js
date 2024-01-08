console.log('carregou')



let selects = document.getElementsByClassName("select-type")

Array.from(selects).forEach((el)=>{
  /* var file= el.target.parentElement.firstChild.nextElementSibling.innerHTML
  console.log(file) */
  el.addEventListener('change', (e)=>{
  
    var file= e.target.parentElement.firstChild.nextElementSibling.innerHTML

    fetch(`/change_types?types=${e.target.value}&file=${file}`, {method: "POST"})

  })
  })




function exibLoader(loader){
 
 document.getElementById(loader).style.display = 'block'
}
document.getElementById('a_convert').addEventListener('click', (e)=> exibLoader('loader_convert')) 
ip = localStorage.getItem('ip')

link = `/getFiles?action=convert&ip=${ip}`
document.getElementById('a_convert').href= link 

