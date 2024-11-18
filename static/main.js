// import Swal from 'sweetalert2'
let datos = [];


document.addEventListener("DOMContentLoaded", function(){
    // make it as accordion for smaller screens
    if (window.innerWidth < 992) {
    
      // close all inner dropdowns when parent is closed
      document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown){
        everydropdown.addEventListener('hidden.bs.dropdown', function () {
          // after dropdown is hidden, then find all submenus
            this.querySelectorAll('.submenu').forEach(function(everysubmenu){
              // hide every submenu as well
              everysubmenu.style.display = 'none';
            });
        })
      });
    
      document.querySelectorAll('.dropdown-menu a').forEach(function(element){
        element.addEventListener('click', function (e) {
            let nextEl = this.nextElementSibling;
            if(nextEl && nextEl.classList.contains('submenu')) {	
              // prevent opening link if link needs to open dropdown
              e.preventDefault();
              if(nextEl.style.display == 'block'){
                nextEl.style.display = 'none';
              } else {
                nextEl.style.display = 'block';
              }
    
            }
        });
      })
    }
    // end if innerWidth
    }); 
    document.addEventListener("DOMContentLoaded", function() {
      // Despliegue del submenú al pasar el mouse
      document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown) {
        everydropdown.addEventListener('mouseover', function(e) {
          let el_link = this.querySelector('.dropdown-toggle');
          let el_menu = this.querySelector('.dropdown-menu');
          el_menu.classList.add('show');
          el_link.setAttribute('aria-expanded', 'true');
        });
        everydropdown.addEventListener('mouseleave', function(e) {
          let el_link = this.querySelector('.dropdown-toggle');
          let el_menu = this.querySelector('.dropdown-menu');
          el_menu.classList.remove('show');
          el_link.setAttribute('aria-expanded', 'false');
        });
      });
    });
    // DOMContentLoaded  end

    window.onload = () => {
      let pagaTotal = 0;
      let listaProductos = [];

      function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length == 2) return parts.pop().split(';').shift();
      }

      const guardarVenta = document.getElementById("guardarVenta");
      guardarVenta.classList.add("d-none");

      guardarVenta.addEventListener("click", () => {
        fetch('/guardarVenta', {
          method: 'POST',
          headers: {  
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({
            'total': pagaTotal,
            'productos': listaProductos
          })
        })
          .then(response => {
            if (!response.ok) throw new Error('Error en la solicitud');
            return response.json();
          })
          .then(data => {
            Swal.fire({
              title: 'Exito!',
              text: 'Venta guardada con exito',
              icon: 'success',
              confirmButtonText: 'Cool'
            }).then(() => {
              // Recarga la página después de hacer clic en "Cool"
              window.location.reload();
            });
      
            console.log("Datos recibidos:", data);
          })
          .catch(error => {
            console.error('Error:', error);
          });
      });
      
      const agregar = document.getElementById("agregar");
      agregar.addEventListener("click", () => {
        const f = document.getElementById("product-form");
        const total = document.getElementById("total-purchase");

        productName = f['product-name'].value.trim();
        quantity = f['product-quantity'].value;
        price = f['product-price'].value;

        if (productName === "" || quantity === "" || price === "") {
          Swal.fire({
            title: 'Error!',
            text: 'Por favor, rellene todos los campos',
            icon: 'error',
            confirmButtonText: 'Cool'
          });
          return;
        }
        else{
          const table = document.getElementById("product-table-body");
          table.innerHTML += `
            <tr>
                <td>${productName}</td>
                <td>${quantity}</td>
                <td>${price}</td>
                <td>${quantity * price}</td>
            </tr>
          `;
  
          pagaTotal += quantity * price;
          total.textContent = pagaTotal.toFixed(2);
          listaProductos.push({
            'name': productName,
            'quantity': quantity,
            'price': price
          });
          if(listaProductos.length > 0){
            guardarVenta.classList.remove("d-none");
          }

          console.log("Productos:", listaProductos);
        }
          
      });
};