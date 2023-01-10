import os
import hashlib

from museum.common.utils import get_file_md5, get_bytes_md5
from museum.common import cache

"""
index_info['module']
{
          "module_name" : "AsymmetricExtremum",
          "module_params" : {
            "window_size" : 128
          }
"""
def by_file_path(file_path, index_info, use_caching):
    # utils.py 파일 전체를 해싱하고 16진수
    file_md5 = get_file_md5(file_path)
    file_name = os.path.split(file_path)[1]
    # cache_path 경로
    cache_path = cache.get_cache_file_path(file_md5, index_info)
    is_cached = cache.check_cached(cache_path)
    # 동일 경로에 동일 파일 존재
    if is_cached:
        samples, feature_size = cache.load_cache(cache_path)
    else:
        # AE.process
        feature_set = set(index_info['module'].process(file_path))
        feature_size = len(feature_set)
        if index_info['use_mod']:
            feature_set = reduce_the_feature_by_mod(feature_set, index_info['use_mod'])
        samples = minhash(feature_set, index_info['num_hash'], index_info['use_smallest'], index_info['use_minmax'])
        if use_caching:
            cache.make_cache(cache_path, samples, feature_size)
    return file_md5, samples, feature_size, file_name

def by_myself(file_path, index_info):

    feature_set = set(index_info['module'].process(file_path))

    return feature_set

def by_file_bytes(args, index_info, use_caching=None):
    file_bytes, target_name = args
    bytes_md5 = get_bytes_md5(file_bytes)
    feature_set = set(index_info['module'].process(file_bytes=file_bytes))
    feature_size = len(feature_set)
    if index_info['use_mod']:
        feature_set = reduce_the_feature_by_mod(feature_set, index_info['use_mod'])
    samples = minhash(feature_set, index_info['num_hash'], index_info['use_smallest'], index_info['use_minmax'])
    return bytes_md5, samples, feature_size, target_name


def minhash(feature_set, num_hash, use_smallest, use_min_max):
    feature_list = list(feature_set)
    # len(feature_list) <= 1
    if len(feature_list) < 1:
        return
    if use_smallest:
        samples = k_smallest(feature_list, num_hash)
    else:
        samples = k_independent(feature_list, num_hash, use_min_max)
    return set(samples)


def k_smallest(feature_list, num_hash):
    int_features = []
    feature_type = type(feature_list[0])
    if feature_type == bytes:
        for i in range(len(feature_list)):
            hashed_feature = hashlib.md5(feature_list[i]).hexdigest()
            int_features.append(int(hashed_feature, 16))
    else:
        for i in range(len(feature_list)):
            hashed_feature = hashlib.md5(feature_list[i].encode()).hexdigest()
            int_features.append(int(hashed_feature, 16))
    int_features = list(set(int_features))
    int_features.sort()
    samples = []
    num_min = min(num_hash, len(int_features))
    for i in range(num_min):
        insert_feature = hex(int_features[i])[2:].rjust(32, '0')
        samples.append(insert_feature)
    return samples


def k_independent(feature_list, num_hash, use_min_max):
    min_hashes = []
    int_min_hashes = []
    for i in range(1, num_hash + 1):
        int_features = []
        feature_type = type(feature_list[0])
        if feature_type == bytes:
            for j in range(len(feature_list)):
                salt_feature = feature_list[j] + bytes(str(i).encode())
                hashed_feature = int(hashlib.md5(salt_feature).hexdigest(), 16)
                int_features.append(hashed_feature)
        else:
            for j in range(len(feature_list)):
                # 128개의 해시함수를 사용하기 위해 str(i) 를 더해 주었다?..
                salt_feature = str(i) + str(i) + feature_list[j] + str(i) + str(i)
                hashed_feature = int(hashlib.md5(salt_feature.encode()).hexdigest(), 16)
                int_features.append(hashed_feature)

        int_features.sort()
        int_min_hashes.append(int_features[0])

        if use_min_max:
            int_min_hashes.append(int_features[-1])
    for int_min_hash in int_min_hashes:
        min_hashes.append(hex(int_min_hash)[2:].rjust(32, '0'))
    return min_hashes


def reduce_the_feature_by_mod(feature, mod_num):
    after_mod_list = []
    feature_list = list(set(feature))
    for feature in feature_list:
        hashed_feature = int(hashlib.md5(feature).hexdigest(), 16)
        if hashed_feature % mod_num == 0:
            after_mod_list.append(feature)
    return after_mod_list

