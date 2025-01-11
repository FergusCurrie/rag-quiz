from crud import create_concept

def test_create_concept(test_db):
    """Test creating a new concept"""
    # Test default case (system-created concept)
    concept = create_concept(test_db)
    assert concept is not None
    assert concept.concept_id is not None
    assert concept.created_date is not None
    assert concept.user_created is False

    # Test user-created concept
    user_concept = create_concept(test_db, user_created=True)
    assert user_concept is not None
    assert user_concept.concept_id is not None
    assert user_concept.created_date is not None
    assert user_concept.user_created is True

    # Verify we have two different concepts
    assert concept.concept_id != user_concept.concept_id
