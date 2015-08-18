#SQLAlchemy <small>Notes</small>

## Part1: Core
  - explanation, reasons to use
  - sqlalchemy engine
  - sql type engine
  - sql expression language
     * select 
     * insert
     * update 
     * functions
  - you can use functions or classes, functional or classical programming
  - examples / praticle use

## Part2: Orm
  - explanation, reasons to use
  - db sessions
  - ext.declarative
     * declarative_base
     * declared_attr
     * BaseModel
  - ext.automap
     * automap_base
  - examples / practicle use

## Part3: Example App
 
  - core version
    - build db with expression language, make a few queries
    
  - orm version
    - build db with orm, make a few queries
    
  - example db structure 

    * projects
      - id int
      - name varchar      
      - due_date date
      - date_added datetime
      - date_modified datetime
      
    * tasks
      - id int
      - name  varchar           
      - project_(id) int
      - due_date date
      - date_added datetime
      - date_modified datetime
      - priority_level_(id) int
      
    * priority_levels
      - id int 
      - name varchar
        
