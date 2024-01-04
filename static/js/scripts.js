console.log('carregou')
document.getElementById("select").addEventListener("change", (e)=>
{
 var file= e.target.parentElement.firstChild.nextElementSibling.innerHTML
 fetch(`/change_types?types=${e.target.value}&file=${file}`, {method: "POST"})
  console.log('mudei'
)
 }
)



function exibLoader(loader){
 
 document.getElementById(loader).style.display = 'block'
}
document.getElementById('a_convert').addEventListener('click', (e)=> exibLoader('loader_convert')) 
