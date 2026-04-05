from flask import Flask, request, jsonify
from gestor import GestorBD
from controladores import ControladorUsuarios, ControladorLotes, ControladorImagenes, ControladorNodos, ControladorLogs

class ServidorREST:
    def __init__(self, host: str = "0.0.0.0", puerto: int = 5000, gestor_bd=None):
        self.host = host
        self.puerto = puerto
        self.gestor_bd = gestor_bd or GestorBD("sqlite:///servidor_bd.db")
        self.app = Flask(__name__)
        
        self.controlador_usuarios = ControladorUsuarios(self.gestor_bd)
        self.controlador_lotes = ControladorLotes(self.gestor_bd)
        self.controlador_imagenes = ControladorImagenes(self.gestor_bd)
        self.controlador_nodos = ControladorNodos(self.gestor_bd)
        self.controlador_logs = ControladorLogs(self.gestor_bd)
        
        self.registrar_rutas()
    
    def registrar_rutas(self):
        
        @self.app.route('/api/usuarios', methods=['POST'])
        def crear_usuario():
            return jsonify(self.controlador_usuarios.crear_usuario(request.json)), 201
        
        @self.app.route('/api/usuarios/<int:id>', methods=['GET'])
        def obtener_usuario(id):
            resultado = self.controlador_usuarios.obtener_usuario(id)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/usuarios/email/<email>', methods=['GET'])
        def obtener_por_email(email):
            resultado = self.controlador_usuarios.obtener_por_email(email)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/usuarios/<int:id>', methods=['PUT'])
        def actualizar_usuario(id):
            resultado = self.controlador_usuarios.actualizar_usuario(id, request.json)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/usuarios/<int:id>', methods=['DELETE'])
        def eliminar_usuario(id):
            self.controlador_usuarios.eliminar_usuario(id)
            return jsonify({"mensaje": "Eliminado"}), 200
        
        @self.app.route('/api/lotes', methods=['POST'])
        def crear_lote():
            return jsonify(self.controlador_lotes.crear_lote(request.json)), 201
        
        @self.app.route('/api/lotes/<int:id>', methods=['GET'])
        def obtener_lote(id):
            resultado = self.controlador_lotes.obtener_lote(id)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/lotes/<int:id>/estado', methods=['PUT'])
        def actualizar_estado_lote(id):
            resultado = self.controlador_lotes.actualizar_estado(id, request.json.get('estado'))
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/usuarios/<int:id>/historial', methods=['GET'])
        def obtener_historial(id):
            return jsonify(self.controlador_lotes.obtener_historial(id))
        
        @self.app.route('/api/imagenes', methods=['POST'])
        def crear_imagen():
            return jsonify(self.controlador_imagenes.crear_imagen(request.json)), 201
        
        @self.app.route('/api/imagenes/<int:id>', methods=['GET'])
        def obtener_imagen(id):
            resultado = self.controlador_imagenes.obtener_imagen(id)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/imagenes/<int:id>', methods=['PUT'])
        def actualizar_imagen(id):
            resultado = self.controlador_imagenes.actualizar_imagen(id, request.json)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/lotes/<int:id>/imagenes', methods=['GET'])
        def obtener_imagenes_por_lote(id):
            return jsonify(self.controlador_imagenes.obtener_por_lote(id))
        
        @self.app.route('/api/nodos', methods=['POST'])
        def registrar_nodo():
            return jsonify(self.controlador_nodos.registrar_nodo(request.json)), 201
        
        @self.app.route('/api/nodos/activos', methods=['GET'])
        def obtener_nodos_activos():
            return jsonify(self.controlador_nodos.obtener_nodos_activos())
        
        @self.app.route('/api/nodos/<int:id>', methods=['GET'])
        def obtener_nodo(id):
            resultado = self.controlador_nodos.obtener_nodo(id)
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/nodos/<int:id>/estado', methods=['PUT'])
        def actualizar_estado_nodo(id):
            resultado = self.controlador_nodos.actualizar_estado(id, request.json.get('estado'))
            return jsonify(resultado) if resultado else jsonify({"error": "No encontrado"}), 404
        
        @self.app.route('/api/logs', methods=['POST'])
        def guardar_log():
            return jsonify(self.controlador_logs.guardar_log(request.json)), 201
        
        @self.app.route('/api/imagenes/<int:id>/logs', methods=['GET'])
        def obtener_logs_imagen(id):
            return jsonify(self.controlador_logs.obtener_logs_imagen(id))
        
        @self.app.route('/api/nodos/<int:id>/logs', methods=['GET'])
        def obtener_logs_nodo(id):
            return jsonify(self.controlador_logs.obtener_logs_nodo(id))
        
        @self.app.route('/api/health', methods=['GET'])
        def health():
            return jsonify({"status": "ok"})
    
    def iniciar(self):
        self.app.run(host=self.host, port=self.puerto, debug=False)
    
    def detener(self):
        print("Deteniendo servidor...")