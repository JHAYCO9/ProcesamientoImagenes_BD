from flask import Flask, request, jsonify
from gestor import GestorBD
from controladores import ControladorUsuarios, ControladorLotes, ControladorImagenes, ControladorNodos, ControladorLogs


class ServidorREST:
    def __init__(self, host: str = "0.0.0.0", puerto: int = 5000, gestor_bd=None):
        self.host = host
        self.puerto = puerto
        self.gestor_bd = gestor_bd or GestorBD("sqlite:///servidor_bd.db")
        self.app = Flask(__name__)

        self.controlador_usuarios  = ControladorUsuarios(self.gestor_bd)
        self.controlador_lotes     = ControladorLotes(self.gestor_bd)
        self.controlador_imagenes  = ControladorImagenes(self.gestor_bd)
        self.controlador_nodos     = ControladorNodos(self.gestor_bd)
        self.controlador_logs      = ControladorLogs(self.gestor_bd)

        self.registrar_rutas()

    def registrar_rutas(self):

        # ── Usuarios ──────────────────────────────────────────

        @self.app.route('/api/login', methods=['POST'])
        def login():
            data     = request.json
            email    = data.get("email")
            password = data.get("password")
            usuario  = self.controlador_usuarios.obtener_por_email(email)
            if not usuario:
                return jsonify({"error": "usuario no existe"}), 404
            from hashlib import sha256
            password_hash = sha256(password.encode()).hexdigest()
            if usuario["password_hash"] != password_hash:
                return jsonify({"error": "password incorrecto"}), 401
            return jsonify({
                "token":   f"TOKEN_{usuario['id_usuario']}",
                "user_id": usuario["id_usuario"]
            })

        @self.app.route('/api/usuarios', methods=['POST'])
        def crear_usuario():
            return jsonify(self.controlador_usuarios.crear_usuario(request.json)), 201

        @self.app.route('/api/usuarios/<int:id>', methods=['GET'])
        def obtener_usuario(id):
            resultado = self.controlador_usuarios.obtener_usuario(id)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/usuarios/email/<email>', methods=['GET'])
        def obtener_por_email(email):
            resultado = self.controlador_usuarios.obtener_por_email(email)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/usuarios/<int:id>', methods=['PUT'])
        def actualizar_usuario(id):
            resultado = self.controlador_usuarios.actualizar_usuario(id, request.json)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/usuarios/<int:id>', methods=['DELETE'])
        def eliminar_usuario(id):
            self.controlador_usuarios.eliminar_usuario(id)
            return jsonify({"mensaje": "Eliminado"}), 200

        @self.app.route('/api/validar_token', methods=['POST'])
        def validar_token():
            token = request.json.get("token")
            if token and token.startswith("TOKEN_"):
                user_id = int(token.split("_")[1])
                return jsonify({"valido": True, "user_id": user_id})
            return jsonify({"valido": False}), 401

        # ── Lotes ─────────────────────────────────────────────

        @self.app.route('/api/lotes', methods=['POST'])
        def crear_lote():
            return jsonify(self.controlador_lotes.crear_lote(request.json)), 201

        @self.app.route('/api/lotes/<int:id>', methods=['GET'])
        def obtener_lote(id):
            resultado = self.controlador_lotes.obtener_lote(id)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/lotes/<int:id>/estado', methods=['PUT'])
        def actualizar_estado_lote(id):
            resultado = self.controlador_lotes.actualizar_estado(id, request.json.get('estado'))
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/lotes/<int:id>/incrementar_completadas', methods=['POST'])
        def incrementar_completadas(id):
            """Incrementa en 1 el contador imagenes_completadas del lote y
            actualiza su estado a COMPLETADO si todas terminaron."""
            resultado = self.controlador_lotes.incrementar_completadas(id)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/usuarios/<int:id>/historial', methods=['GET'])
        def obtener_historial(id):
            return jsonify(self.controlador_lotes.obtener_historial(id))

        # ── Imágenes ──────────────────────────────────────────

        @self.app.route('/api/imagenes', methods=['POST'])
        def crear_imagen():
            return jsonify(self.controlador_imagenes.crear_imagen(request.json)), 201

        @self.app.route('/api/imagenes/<int:id>', methods=['GET'])
        def obtener_imagen(id):
            resultado = self.controlador_imagenes.obtener_imagen(id)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/imagenes/<int:id>', methods=['PUT'])
        def actualizar_imagen(id):
            resultado = self.controlador_imagenes.actualizar_imagen(id, request.json)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/lotes/<int:id>/imagenes', methods=['GET'])
        def obtener_imagenes_por_lote(id):
            return jsonify(self.controlador_imagenes.obtener_por_lote(id))

        @self.app.route('/api/transformaciones', methods=['POST'])
        def crear_transformacion():
            return jsonify(self.controlador_imagenes.crear_transformacion(request.json)), 201

        @self.app.route('/api/transformaciones/<int:id>', methods=['PUT'])
        def actualizar_transformacion(id):
            resultado = self.controlador_imagenes.actualizar_transformacion(id, request.json)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        # ── Nodos ─────────────────────────────────────────────

        @self.app.route('/api/nodos', methods=['POST'])
        def registrar_nodo():
            return jsonify(self.controlador_nodos.registrar_nodo(request.json)), 201

        @self.app.route('/api/nodos', methods=['GET'])
        def listar_nodos():
            """Lista todos los nodos con su estado (ACTIVO/INACTIVO/ERROR)."""
            return jsonify(self.controlador_nodos.listar_todos())

        @self.app.route('/api/nodos/activos', methods=['GET'])
        def obtener_nodos_activos():
            return jsonify(self.controlador_nodos.obtener_nodos_activos())

        @self.app.route('/api/nodos/<int:id>', methods=['GET'])
        def obtener_nodo(id):
            resultado = self.controlador_nodos.obtener_nodo(id)
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        @self.app.route('/api/nodos/<int:id>/estado', methods=['PUT'])
        def actualizar_estado_nodo(id):
            resultado = self.controlador_nodos.actualizar_estado(id, request.json.get('estado'))
            if resultado:
                return jsonify(resultado)
            return jsonify({"error": "No encontrado"}), 404

        # ── Logs ──────────────────────────────────────────────

        @self.app.route('/api/logs', methods=['POST'])
        def guardar_log():
            return jsonify(self.controlador_logs.guardar_log(request.json)), 201

        @self.app.route('/api/imagenes/<int:id>/logs', methods=['GET'])
        def obtener_logs_imagen(id):
            return jsonify(self.controlador_logs.obtener_logs_imagen(id))

        @self.app.route('/api/nodos/<int:id>/logs', methods=['GET'])
        def obtener_logs_nodo(id):
            return jsonify(self.controlador_logs.obtener_logs_nodo(id))

        # ── Health ────────────────────────────────────────────

        @self.app.route('/api/health', methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

    def iniciar(self):
        self.app.run(host=self.host, port=self.puerto, debug=False)

    def detener(self):
        print("Deteniendo servidor...")