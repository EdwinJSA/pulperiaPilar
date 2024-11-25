// import Swal from 'sweetalert2'
let datos = [];
let clientes = [];

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length == 2) return parts.pop().split(';').shift();
}

document.addEventListener("DOMContentLoaded", function () {
  // make it as accordion for smaller screens
  if (window.innerWidth < 992) {

    // close all inner dropdowns when parent is closed
    document.querySelectorAll('.navbar .dropdown').forEach(function (everydropdown) {
      everydropdown.addEventListener('hidden.bs.dropdown', function () {
        // after dropdown is hidden, then find all submenus
        this.querySelectorAll('.submenu').forEach(function (everysubmenu) {
          // hide every submenu as well
          everysubmenu.style.display = 'none';
        });
      })
    });

    document.querySelectorAll('.dropdown-menu a').forEach(function (element) {
      element.addEventListener('click', function (e) {
        let nextEl = this.nextElementSibling;
        if (nextEl && nextEl.classList.contains('submenu')) {
          // prevent opening link if link needs to open dropdown
          e.preventDefault();
          if (nextEl.style.display == 'block') {
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
document.addEventListener("DOMContentLoaded", function () {
  // Despliegue del submenú al pasar el mouse
  document.querySelectorAll('.navbar .dropdown').forEach(function (everydropdown) {
    everydropdown.addEventListener('mouseover', function (e) {
      let el_link = this.querySelector('.dropdown-toggle');
      let el_menu = this.querySelector('.dropdown-menu');
      el_menu.classList.add('show');
      el_link.setAttribute('aria-expanded', 'true');
    });
    everydropdown.addEventListener('mouseleave', function (e) {
      let el_link = this.querySelector('.dropdown-toggle');
      let el_menu = this.querySelector('.dropdown-menu');
      el_menu.classList.remove('show');
      el_link.setAttribute('aria-expanded', 'false');
    });
  });
});
// DOMContentLoaded  end

/*window.onload = () => {
  let pagaTotal = 0;
  let listaProductos = [];

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
          confirmButtonText: 'Aceptar'
        }).then(() => {
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
        confirmButtonText: 'Aceptar'
      });
      return;
    }
    else {
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
      if (listaProductos.length > 0) {
        guardarVenta.classList.remove("d-none");
      }

      console.log("Productos:", listaProductos);
    }

  });
};*/

document.addEventListener('DOMContentLoaded', function () {
  // Código del script main.js o producto.js
  document.addEventListener('keyup', e => {
    if (e.target.matches("#inputProduct")) {
      if (e.key === 'Escape') e.target.value = '';
      document.querySelectorAll('.articulo').forEach(producto => {
        producto.textContent.toLowerCase().includes(e.target.value.toLowerCase())
          ? producto.classList.remove('d-none')
          : producto.classList.add('d-none');
      });
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const editarBtns = document.querySelectorAll('#btn-editar');

  editarBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const codigo = this.getAttribute('data-codigo');
      const nombre = this.getAttribute('data-nombre');
      const precio = this.getAttribute('data-precio');
      const cantidad = this.getAttribute('data-cantidad');
      const categoria = this.getAttribute('data-categoria');
      const descripcion = this.getAttribute('data-descripcion');

      document.getElementById('codigo').value = codigo;
      document.getElementById('nombre').value = nombre;
      document.getElementById('precio').value = precio;
      document.getElementById('cantidad').value = cantidad;
      document.getElementById('categoria').value = categoria;
      document.getElementById('descripcion').value = descripcion;

      const modal = new bootstrap.Modal(document.getElementById('modalEditar'));
      modal.show();
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const guardarCambios = document.getElementById('guardarCambios');

  guardarCambios.addEventListener('click', function (event) {
    // Evita la acción predeterminada de enviar el formulario
    event.preventDefault();

    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const cant = document.getElementById('cantidad').value;
    const categoria = document.getElementById('categoria').value;
    const descripcion = document.getElementById('descripcion').value;

    fetch('/actualizar_producto', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        'codigo': codigo,
        'nombre': nombre,
        'precio': precio,
        'cantidad': cant,
        'categoria': categoria,
        'descripcion': descripcion
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        Swal.fire({
          title: 'Éxito!',
          text: 'Producto actualizado correctamente',
          icon: 'success',
          confirmButtonText: 'Aceptar'
        }).then(() => {
          // Recarga la página después de que el usuario haga clic en "Aceptar"
          location.reload();
        });
      })
      .catch(error => {
        console.error('Error:', error);
        Swal.fire({
          title: 'Error!',
          text: 'Error al actualizar el producto',
          icon: 'error',
          confirmButtonText: 'Aceptar'
        });
      });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const eliminarBtns = document.querySelectorAll('#btn-eliminar');

  eliminarBtns.forEach(function (btn) {
    btn.addEventListener('click', function (event) {
      const productoId = btn.getAttribute('data-producto-id');

      Swal.fire({
        title: '¿Estás seguro?',
        text: 'Este producto será eliminado permanentemente.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/eliminar_producto/${productoId}`, {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': getCookie('csrftoken')
            }
          })
            .then(response => response.json())
            .then(data => {
              console.log(data);
              Swal.fire({
                title: 'Éxito!',
                text: 'Producto eliminado correctamente',
                icon: 'success',
                confirmButtonText: 'Aceptar'
              }).then(() => {
                // Recarga la página luego de que el usuario haga clic en "Aceptar"
                location.reload();
              });
            })
            .catch(error => {
              console.error('Error:', error);
              Swal.fire({
                title: 'Error!',
                text: error.message,
                icon: 'error',
                confirmButtonText: 'Aceptar'
              });
            });
        }
      });
    });
  });
});
//busqueda de clientes
document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('keyup', e => {
    if (e.target.matches("#inputClient")) {
      if (e.key === 'Escape') e.target.value = '';
      document.querySelectorAll('.us_cliente').forEach(cliente => {
        cliente.textContent.toLowerCase().includes(e.target.value.toLowerCase())
          ? cliente.classList.remove('d-none')
          : cliente.classList.add('d-none');
      });
    }
  });
});

//busqueda de proveedores
document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('keyup', e => {
    if (e.target.matches("#inputProvider")) {
      if (e.key === 'Escape') e.target.value = '';
      document.querySelectorAll('.us_proveedor').forEach(proveedor => {
        proveedor.textContent.toLowerCase().includes(e.target.value.toLowerCase())
          ? proveedor.classList.remove('d-none')
          : proveedor.classList.add('d-none');
      });
    }
  });
});
document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('keyup', e => {
    if (e.target.matches("#inputClientCredito")) {
      if (e.key === 'Escape') e.target.value = '';
      document.querySelectorAll('.tabla_credito').forEach(cliente => {
        cliente.textContent.toLowerCase().includes(e.target.value.toLowerCase())
          ? cliente.classList.remove('d-none')
          : cliente.classList.add('d-none');
      });
    }
  });
});



const btnCreditoCliente = document.getElementById('creditoCliente');

btnCreditoCliente.addEventListener('click', () => {
  const cliente = document.getElementById('nombreClienteAbon').value;

  fetch('/creditoCliente', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      'cliente': cliente
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      Swal.fire({
        title: 'Éxito!',
        text: 'Credito asignado correctamente',
        icon: 'success',
        confirmButtonText: 'Aceptar'
      })
      .then(() => {
        
      });
    })
});