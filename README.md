# README
# T-shirts DB

## users table

|Column|Type|Options|
|------|----|-------|
|email|string|null: false|
|password|string|null: false|
|name|string|null: false|
### Association
- has_many tshirts

## tshirts table
|Column|Type|Options|
|------|----|-------|
|image|text||
|comment|text||
|user_id|integer|null: false, foreign_key: true|
|price_id|integer|null: false, foreign_key: true|
### Association
- belongs_to user
- belongs_to price

## prices table
|Column|Type|Options|
|------|----|-------|
|name|sring|null: false|
### Association
- has_many tshirts