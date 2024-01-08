function getIPFromAmazon() {
    fetch("https://api.ipify.org?format=json").then(res => res.text()).then(data => 
    {localStorage.setItem('ip', JSON.parse(data).ip)

    document.getElementById('ip').value = localStorage.getItem('ip')
   
})
    
  }
  
  getIPFromAmazon()




 