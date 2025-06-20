function createNetwork(graph) {
    // Netzwerk-Container

    const nodes = new vis.DataSet(graph.nodes)
     
    // Kanten
    const edges = new vis.DataSet(graph.edges);

    // Konfiguration
    const container = document.getElementById('network');
    const data = {
      nodes: nodes,
      edges: edges
    };
    const options = {
      nodes: {
        shapeProperties: {
          useImageSize: false, // Nutzt Originalgröße des SVGs
        },
        size: 15,
        font: {
          size: 12
        }
      },
      edges: {
        arrows: {
          to: { enabled: true, scaleFactor: 0.6 }
        },
        font: {
          size: 10,        // kleinere Schrift für Edges
          align: 'middle'
        }
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          springLength: 150, // Längere Feder für größere Abstände
          springConstant: 0.01, // Geringere Federkonstante für san
        },
        stabilization: {
          iterations: 200
        }
      }
    };

    // Netzwerk erstellen
    const network = new vis.Network(container, data, options);


    network.on("dragEnd", function (params) {
      if (params.nodes.length > 0) {
        const id = params.nodes[0];
        const pos = network.getPositions([id]);
        console.log(`Knoten ${id} neue Position:`, pos[id]);
      }
    });


}

$(document).ready(function() {




    // API Call mit getJSON
    $.getJSON('/graph/', function(data) {
        console.log(data);
        // Netzwerk aufbauen
        createNetwork(data);

    }).fail(function(jqxhr, textStatus, error) {
        console.log("Error: " + textStatus + ", " + error);
    });
});
   