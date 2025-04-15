//alert("fetchData");

let dataReady = false;
let datos = {}

document.addEventListener('DOMContentLoaded', fetchData);

function fetchData() {
    // Primero, añadimos los estilos CSS al head del documento
    const style = document.createElement('style');
    style.textContent = `
  .charts-main-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
  }
  
  .chart-item {
    width: 500px;
    height: 500px;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    background-color: white;
    margin-bottom: 20px;
  }
  
  @media (max-width: 1100px) {
    .chart-item {
      width: 100%;
      max-width: 600px;
    }
  }
`;
    document.head.appendChild(style);

    // Creamos un contenedor principal para todos los gráficos
    const mainContainer = document.createElement('div');
    mainContainer.className = 'charts-main-container';
    document.body.appendChild(mainContainer);

    // Ahora modificamos tu código original
    fetch('/get_data?title=' + filename)
        .then(response => response.json())
        .then(data => {
            //console.log(data);
            datos = data;

            // Indicar que los datos están listos
            dataReady = true;
            showContent();

            datos.suggested_graphics.forEach(suggestedGraphic => {

                // Crear contenedor para este gráfico
                const chartItem = document.createElement('div');
                chartItem.className = 'chart-item';

                // Crear el canvas dentro del contenedor
                const newCanvas = document.createElement('canvas');
                newCanvas.id = 'chart-' + Math.random().toString(36).substr(2, 9); // ID único
                chartItem.appendChild(newCanvas);

                // Añadir el contenedor al contenedor principal
                mainContainer.appendChild(chartItem);

                // Crear el gráfico
                const newCtx = newCanvas.getContext('2d');


                if (suggestedGraphic.tipo == 'pie' || suggestedGraphic.tipo == 'bar') {
                    let graphicType = suggestedGraphic.tipo;
                    //console.log(graphicType);

                    let labelsList = datos.data.map(record => record[suggestedGraphic.fields[0]]);
                    let labels = [];
                    datos.data.map(record => record[suggestedGraphic.fields[0]]).forEach(element => {
                        if (!labels.includes(element)) {
                            labels.push(element);
                        }
                    });

                    let qtyPerLabel = [];
                    let avgs = [];

                    labels.forEach(element => {
                        let qty = datos.data.map(record => record[suggestedGraphic.fields[0]]).filter(record => record == element).length;
                        qtyPerLabel.push(qty);
                        if (suggestedGraphic.fields.length > 1) {
                            let countables = datos.data.filter(record => record[suggestedGraphic.fields[0]] == element).map(record => record[suggestedGraphic.fields[1]]);
                            let sum_countables = countables.reduce((acc, currentValue) => acc + currentValue, 0);
                            let avg_countables = sum_countables / countables.length;
                            avgs.push(avg_countables);
                            //console.log((countables.reduce((acc, currentValue) => acc + currentValue, 0)) / countables.length);
                        }
                    });

                    //console.log("avgs", avgs);
                    let graphicData = {
                        labels: labels,
                        datasets: [{
                            label: 'Ventas',
                            data: qtyPerLabel,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.7)',
                                'rgba(54, 162, 235, 0.7)',
                                'rgba(255, 206, 86, 0.7)',
                                'rgba(75, 192, 192, 0.7)',
                                'rgba(153, 102, 255, 0.7)',
                                'rgba(255, 159, 64, 0.7)'
                            ],
                            borderColor: [
                                'rgb(255, 99, 132)',
                                'rgb(54, 162, 235)',
                                'rgb(255, 206, 86)',
                                'rgb(75, 192, 192)',
                                'rgb(153, 102, 255)',
                                'rgb(255, 159, 64)'
                            ],
                            borderWidth: 1
                        }]
                    };

                    if (avgs.length > 0) {
                        graphicData.datasets[0].data = avgs;
                        //console.log("graphicData", graphicData);
                    }

                    new Chart(newCtx, {
                        type: graphicType,
                        data: graphicData,
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            plugins: {
                                title: {
                                    display: true,
                                    text: suggestedGraphic.titulo
                                },
                                legend: {
                                    position: 'bottom'
                                }
                            }
                        }
                    });
                }
                else if (suggestedGraphic.tipo == 'scatter') {
                    //grafico de prueba
                    let graphicType = suggestedGraphic.tipo;
                    let fields = suggestedGraphic.fields
                    let graphicData = datos.data.map(record => ({
                        x: record[fields[0]],
                        y: record[fields[1]]
                    }))
                    const data = {
                        datasets: [{
                            data: graphicData,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)'
                        }]
                    };

                    // Configuración del gráfico
                    const config = {
                        type: 'scatter',
                        data: data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            plugins: {
                                title: {
                                    display: true,
                                    text: suggestedGraphic.titulo
                                },
                                legend: {
                                    position: 'bottom',
                                },
                            },
                            scales: {   
                                x: {
                                    title: {
                                        display: true,
                                        text: fields[0]
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: fields[1]
                                    }
                                }
                            }
                        }
                    };


                    new Chart(newCtx, config);

                    //console.log('Insertar grafico de dispersion');
                    // Implementar lógica para gráfico scatter si es necesario
                }
                /*else if (suggestedGraphic.tipo == 'line') {
                    // grafico de linea de prueba
                    new Chart(newCtx, {
                            type: 'line', // tipo de gráfico
                            data: {
                              labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'], // eje X
                              datasets: [{
                                label: 'Horas de estudio',
                                data: [2, 4, 3, 5, 6], // eje Y
                                borderColor: 'blue',
                                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                                fill: true, // para que se vea el color debajo de la línea
                                tension: 0.3 // suaviza la curva
                              }]
                            },
                        }
                    )
                }*/
            });
        });
}