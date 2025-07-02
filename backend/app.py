from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///./feature_flags.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FeatureFlag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    user_segment = db.Column(db.String(255), default='all')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'user_segment': self.user_segment
        }

@app.route('/features', methods=['GET'])
def get_features():
    features = FeatureFlag.query.all()
    return jsonify([feature.to_dict() for feature in features])

@app.route('/features/<name>', methods=['GET'])
def get_feature(name):
    feature = FeatureFlag.query.filter_by(name=name).first()
    if not feature:
        return jsonify({'message': 'Feature not found'}), 404
    return jsonify(feature.to_dict())

@app.route('/features', methods=['POST'])
def create_feature():
    data = request.get_json()
    new_feature = FeatureFlag(
        name=data['name'],
        description=data.get('description', ''),
        is_active=data.get('is_active', False),
        user_segment=data.get('user_segment', 'all')
    )
    db.session.add(new_feature)
    db.session.commit()
    return jsonify(new_feature.to_dict()), 201

@app.route('/features/<name>', methods=['PUT'])
def update_feature(name):
    feature = FeatureFlag.query.filter_by(name=name).first()
    if not feature:
        return jsonify({'message': 'Feature not found'}), 404
    data = request.get_json()
    feature.description = data.get('description', feature.description)
    feature.is_active = data.get('is_active', feature.is_active)
    feature.user_segment = data.get('user_segment', feature.user_segment)
    db.session.commit()
    return jsonify(feature.to_dict())

@app.route('/features/<name>', methods=['DELETE'])
def delete_feature(name):
    feature = FeatureFlag.query.filter_by(name=name).first()
    if not feature:
        return jsonify({'message': 'Feature not found'}), 404
    db.session.delete(feature)
    db.session.commit()
    return jsonify({'message': 'Feature deleted'})

if __name__ == '__main__':
    app.run(debug=True)
