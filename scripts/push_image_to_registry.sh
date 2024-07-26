#!/usr/bin/bash
set -e

source "./pushed_image.sh"

addrs=(
    "192.168.26.85:5000"
    "192.168.26.244:8443"
)


push_image() {
    for image in "${images[@]}"; do
        echo "pulling $image ..."
        docker pull "$image"
        if [[ "$image" == *"."*/* ]]; then
            baseimage="${image#*/}"
            echo $image $baseimage
        else
            baseimage="$image"
        fi
        for ip in "${addrs[@]}"; do
            echo "pusing image: $ip/$baseimage"
            docker tag "$image" "$ip"/"$baseimage"
            docker push "$ip"/"$baseimage"
        done
    done
}

interactive_delete_image() {
    docker exec -it registry /bin/sh
    cd /var/lib/registry/docker/registry/v2/repositories/
    # rm -rf xxx
    registry garbage-collect /etc/docker/registry/config.yml
    image=pause
    tag=3.9
    digest=$(curl -sS -k -H "Accept: application/vnd.docker.distribution.manifest.v2+json" "https://localhost/v2/$image/manifests/$tag" | jq -r '.config.digest')
    echo $digest
}

push_image
