from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import json

class RealTimeManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_users = {}
        self.project_rooms = set()
        
        # Register event handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            print(f"Client connected: {request.sid}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self._remove_user(request.sid)
            print(f"Client disconnected: {request.sid}")
        
        @self.socketio.on('join')
        def handle_join(data):
            user_id = data.get('user_id')
            role = data.get('role')
            self._add_user(request.sid, user_id, role)
            
            # Join role-specific room
            join_room(role)
            
            # If user is investor or fund seeker, join their specific projects
            if 'projects' in data:
                for project_id in data['projects']:
                    join_room(f"project_{project_id}")
                    self.project_rooms.add(f"project_{project_id}")
        
        @self.socketio.on('leave')
        def handle_leave(data):
            role = data.get('role')
            leave_room(role)
            
            if 'projects' in data:
                for project_id in data['projects']:
                    leave_room(f"project_{project_id}")
    
    def _add_user(self, sid, user_id, role):
        self.active_users[sid] = {
            'user_id': user_id,
            'role': role,
            'connected_at': datetime.now().isoformat()
        }
    
    def _remove_user(self, sid):
        if sid in self.active_users:
            del self.active_users[sid]
    
    # Project Updates
    def notify_project_update(self, project_id, update_type, data):
        """Notify all relevant parties about project updates"""
        room = f"project_{project_id}"
        self.socketio.emit('project_update', {
            'project_id': project_id,
            'type': update_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }, room=room)
        
        # Also notify admins
        self.socketio.emit('project_update', {
            'project_id': project_id,
            'type': update_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }, room='admin')
    
    def notify_funding_update(self, project_id, amount, investor_id):
        """Notify about new investments"""
        self.notify_project_update(project_id, 'funding', {
            'amount': amount,
            'investor_id': investor_id
        })
    
    def notify_status_change(self, project_id, new_status):
        """Notify about project status changes"""
        self.notify_project_update(project_id, 'status', {
            'new_status': new_status
        })
    
    def notify_esg_update(self, project_id, new_score):
        """Notify about ESG score updates"""
        self.notify_project_update(project_id, 'esg', {
            'new_score': new_score
        })
    
    # User Management Updates
    def notify_user_status_change(self, user_id, new_status):
        """Notify admins about user status changes"""
        self.socketio.emit('user_update', {
            'user_id': user_id,
            'type': 'status',
            'new_status': new_status,
            'timestamp': datetime.now().isoformat()
        }, room='admin')
    
    # System Updates
    def notify_system_status(self, component, status, message):
        """Notify admins about system status changes"""
        self.socketio.emit('system_update', {
            'component': component,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }, room='admin')
    
    # Analytics Updates
    def broadcast_analytics_update(self, update_type, data):
        """Broadcast analytics updates to admins"""
        self.socketio.emit('analytics_update', {
            'type': update_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }, room='admin')
    
    # ESG Parameter Updates
    def notify_esg_parameter_change(self, new_params):
        """Notify all users about ESG parameter changes"""
        self.socketio.emit('esg_params_update', {
            'params': new_params,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
    
    def get_active_users(self):
        """Get list of currently active users"""
        return self.active_users
    
    def get_project_rooms(self):
        """Get list of active project rooms"""
        return list(self.project_rooms)
