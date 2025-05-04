"""
Example script demonstrating how to use the generated Python SDK
to interact with the Content Publishing Platform's API.
"""

from moderation_sdk.api.posts_api import PostsApi
from moderation_sdk.model.post_create import PostCreate
from moderation_sdk.model.post_update import PostUpdate
from moderation_sdk import ApiClient, Configuration

def main():
    # Configure the API client
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(config)
    
    # Create an instance of the PostsApi
    api = PostsApi(client)
    
    print("Content Publishing Platform SDK Example")
    print("======================================")
    
    try:
        # Create a new draft post
        print("\n1. Creating a new draft post...")
        
        new_post = PostCreate(
            title="Sample SDK Post",
            content="This is a post created using the Python SDK. It demonstrates how to programmatically interact with the Content Publishing Platform API. This content is long enough to pass the minimum length check."
        )
        
        created_post = api.create_post(new_post)
        post_id = created_post.id
        print(f"Post created with ID: {post_id}")
        print(f"Status: {created_post.status}")
        
        # Update the post
        print("\n2. Updating the post...")
        
        updated_post_data = PostUpdate(
            title="Updated SDK Post",
            content="This is an updated post using the Python SDK. It demonstrates how to programmatically update content through the API. The content has been modified to show this functionality in action."
        )
        
        updated_post = api.update_post(post_id, updated_post_data)
        print(f"Post updated: {updated_post.title}")
        
        # Submit the post for review
        print("\n3. Submitting post for review...")
        
        reviewed_post = api.submit_post_for_review(post_id)
        print(f"Post review status: {reviewed_post.status}")
        
        if reviewed_post.status == "flagged":
            print(f"Post was flagged for: {reviewed_post.flagged_reasons}")
            
            # If flagged, update to fix issues
            print("\n4. Fixing flagged issues...")
            fixed_post_data = PostUpdate(
                content="This is a corrected post using the Python SDK. It demonstrates how to fix issues that were flagged during content moderation. The content has been modified to comply with platform guidelines."
            )
            
            fixed_post = api.update_post(post_id, fixed_post_data)
            print("Post updated to fix issues")
            
            # Resubmit
            print("\n5. Resubmitting post for review...")
            reviewed_post = api.submit_post_for_review(post_id)
            print(f"Post review status: {reviewed_post.status}")
        
        # If approved, publish the post
        if reviewed_post.status == "approved":
            print("\n6. Publishing approved post...")
            published_post = api.publish_post(post_id)
            print(f"Post published successfully. Status: {published_post.status}")
        
        # Get all posts
        print("\n7. Listing all posts...")
        posts = api.read_posts()
        print(f"Total posts: {len(posts)}")
        
        for i, post in enumerate(posts):
            print(f"Post {i+1}: {post.title} (Status: {post.status})")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    print("\nSDK Example completed!")

if __name__ == "__main__":
    main()
