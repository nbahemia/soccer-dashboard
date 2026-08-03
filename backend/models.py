from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ------------------------------------------------
# League
# Creates a league table
# Teams and players are associated with the league
# ------------------------------------------------

class League(db.Model):
    __tablename__ = 'leagues'

    league_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    
    teams = db.relationship('Team', backref='league', lazy=True)
    
    def to_dict(self):
        return {
            'league_id': self.league_id,
            'name': self.name,
            'country': self.country
        }
    
# ------------------------------------------------
# Team
# Creates a team table
# Players are associated with the team
# ------------------------------------------------

class Team(db.Model):
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.league_id'), nullable=False)
    
    players = db.relationship('Player', backref='team', lazy=True)
    
    def to_dict(self):
        return {
            'team_id': self.team_id,
            'name': self.name,
            'league_id': self.league_id
        }
        
# ------------------------------------------------
# Player
# Creates a player table
# Players are associated with the team
# ------------------------------------------------

class Player(db.Model):
    __tablename__ = 'players'
    
    # ID keys for the player
    player_id = db.Column(db.Integer, primary_key=True)
    fbref_id = db.Column(db.String(100), nullable=False)

    # Player information
    name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    
    # Positional Information
    raw_position = db.Column(db.String(100), nullable=False)
    primary_position = db.Column(db.String(100), nullable=False)
    secondary_position = db.Column(db.String(100), nullable=True)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    
    def to_dict(self):
        return {
            'player_id': self.player_id,
            'fbref_id': self.fbref_id,
            'name': self.name,
            'nationality': self.nationality,
            'date_of_birth': self.date_of_birth,
            'raw_position': self.raw_position,
            'primary_position': self.primary_position,
            'secondary_position': self.secondary_position,
            'team_id': self.team_id,
        }

# ------------------------------------------------
# Stats
# Creates a stats table
# Stats are associated with the player
# ------------------------------------------------

class Stats(db.Model):
    __tablename__ = 'stats'
    
    stats_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    
    # Standard Statistics -- Whole and per 90
    matches_played = db.Column(db.Integer, nullable=False)
    starts = db.Column(db.Integer, nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    goals_plus_assists = db.Column(db.Integer, nullable=False)
    non_penalty_goals = db.Column(db.Integer, nullable=False)
    penalties_goals = db.Column(db.Integer, nullable=False)
    penalties_taken = db.Column(db.Integer, nullable=False)
    yellow_cards = db.Column(db.Integer, nullable=False)
    red_cards = db.Column(db.Integer, nullable=False)
    
    goals_per_90 = db.Column(db.Float, nullable=False)
    assists_per_90 = db.Column(db.Float, nullable=False)
    goals_plus_assists_per_90 = db.Column(db.Float, nullable=False)
    non_penalty_goals_per_90 = db.Column(db.Float, nullable=False)
    non_penalty_goals_plus_assists_per_90 = db.Column(db.Float, nullable=False)

    # Shooting Statistics
    shots = db.Column(db.Integer, nullable=False)
    shots_on_target = db.Column(db.Integer, nullable=False)
    shots_on_target_percentage = db.Column(db.Float, nullable=True)
    shots_per_90 = db.Column(db.Float, nullable=False)
    shots_on_target_per_90 = db.Column(db.Float, nullable=False)
    goals_per_shot = db.Column(db.Float, nullable=True)
    goals_per_shot_on_target = db.Column(db.Float, nullable=True)
    
    # Creation Statistics
    xG = db.Column(db.Float, nullable=True)
    NPxG = db.Column(db.Float, nullable=True)
    xA = db.Column(db.Float, nullable=True)
    xGChain = db.Column(db.Float, nullable=True)
    xGBuildup = db.Column(db.Float, nullable=True)
    XG90 = db.Column(db.Float, nullable=True)
    NPxG90 = db.Column(db.Float, nullable=True)
    XA90 = db.Column(db.Float, nullable=True)
    xG90_plus_xA90 = db.Column(db.Float, nullable=True)
    NPxG90_plus_XA90 = db.Column(db.Float, nullable=True)
    xGChain90 = db.Column(db.Float, nullable=True)
    xGBuildup90 = db.Column(db.Float, nullable=True)
    
    
    # Goalkeeping
    goals_conceded = db.Column(db.Integer, nullable=True)
    goals_conceded_per_90 = db.Column(db.Float, nullable=True)
    shots_on_target_against = db.Column(db.Integer, nullable=True)
    saves = db.Column(db.Integer, nullable=True)
    save_percentage = db.Column(db.Float, nullable=True)
    clean_sheets = db.Column(db.Integer, nullable=True)
    clean_sheets_percentage = db.Column(db.Float, nullable=True)
    
    
    __table_args__ = (
        db.UniqueConstraint('player_id', 'season', name='uq_stats_player_season'),
    )