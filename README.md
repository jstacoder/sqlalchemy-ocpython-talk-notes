##SqlAlchemy Notes

## part1: Core
    - explanation, reasons to use
    - sqlalchemy engine
    - sql type engine
    - sql expression language
        * select 
        * insert
        * update 
        * functions
    - examples / praticle use

## part2: Orm
    - explanation, reasons to use
    - db sessions
    - ext.declarative
        * declarative_base
        * declared_attr
        * BaseModel
    - ext.automap
        * automap_base
    - examples / practicle use

## part3: example app
 
    - core version
    - orm version 

        * projects
            - id
            - name
            - tasks
            - due_date
            - date_added
            - date_modified
        * tasks
            - id
            - name             
            - project (id)
            - due_date
            - date_added
            - date_modified
            - priority_level (id)
        * priority_levels
            - id
            - name
        
