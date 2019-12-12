import traceback

from reclaimer.sounds import util, constants

__all__ = ("compile_sound", "compile_pitch_range",)


def compile_pitch_range(pitch_range, blam_pitch_range,
                        channel_count, sample_rate, ignore_size_limits=False):
    '''
    Compiles the provided BlamSoundPitchRange into the
    provided snd! pitch range block.
    '''
    errors = []

    # make sure the imported sounds are the correct
    # encoding, sample rate, and have a valid compression.
    for name, blam_sound_perm in blam_pitch_range.permutations.items():
        blam_channel_count = constants.channel_counts.get(
            blam_sound_perm.encoding, "invalid")

        if sample_rate != blam_sound_perm.sample_rate:
            errors.append('Cannot add %skHz sounds to %skHz tag.' %
                          (blam_sound_perm.sample_rate, sample_rate))

        if channel_count != blam_channel_count:
            errors.append('Cannot add %s channel sounds to %s channel tag.' %
                          (blam_channel_count, sample_rate))

        if blam_sound_perm.compression not in (constants.COMPRESSION_PCM_16_LE,
                                               constants.COMPRESSION_PCM_16_BE,
                                               constants.COMPRESSION_ADPCM,
                                               constants.COMPRESSION_OGG):
            errors.append('Unknown permutation compression "%s"' %
                          blam_sound_perm.compression)

        for blam_samples in blam_sound_perm.processed_samples:
            if len(blam_samples.sample_data) > constants.MAX_SAMPLE_CHUNK_SIZE:
                errors.append('Sample data too large to compile in "%s"' % name)

            if len(blam_samples.mouth_data) > constants.MAX_MOUTH_DATA:
                errors.append('Mouth data too large to compile in "%s"' % name)

    if errors:
        return errors

    snd__perms = pitch_range.permutations.STEPTREE
    snd__perm_names = set()
    # loop over the permutations blam_samples and string
    # them together into lists of permutation blocks
    for blam_perm_name in sorted(blam_pitch_range.permutations):
        blam_sound_perm = blam_pitch_range.permutations[blam_perm_name]
        name = get_unique_name_31char(blam_perm_name.strip().lower(),
                                      snd__perm_names)
        snd__perm_names.add(name)

        snd__perm_chain = []
        try:
            for blam_samples in blam_sound_perm.processed_samples:
                snd__perms.append()  # create the new perm block
                snd__perm, _ = snd__perms.pop(-1)
                snd__perm.name = name

                if blam_samples.compression == constants.COMPRESSION_ADPCM:
                    snd__perm.compression.set_to("xbox_adpcm")
                elif blam_samples.compression == constants.COMPRESSION_OGG:
                    snd__perm.compression.set_to("ogg")
                else:
                    snd__perm.compression.set_to("none")

                snd__perm.name = name
                snd__perm.ogg_sample_count = blam_samples.sample_count
                snd__perm.samples.data = blam_samples.sample_data
                snd__perm.mouth_data.data = blam_samples.mouth_data

                snd__perm_chain.append(snd__perm)

            errors.extend(
                merge_permutation_chain(
                    snd__perm_chain, pitch_range, ignore_size_limits)
                )
        except Exception:
            errors.append(traceback.format_exc())
            errors.append("Could not compile permutation '%s'" % blam_perm_name)

    return errors


def compile_sound(snd__tag, blam_sound_bank, ignore_size_limits=False,
                  update_mode=constants.SOUND_COMPILE_MODE_PRESERVE):
    assert update_mode in (constants.SOUND_COMPILE_MODE_NEW,
                           constants.SOUND_COMPILE_MODE_PRESERVE,
                           constants.SOUND_COMPILE_MODE_ADDITIVE)
    errors = []
    tagdata = snd__tag.data.tagdata
    if update_mode == constants.SOUND_COMPILE_MODE_NEW:
        # clear the old contents of the tag
        tagdata.parse()
        if blam_sound_bank.generate_mouth_data:
            tagdata.sound_class.set_to("unit_dialog")

    if update_mode != constants.SOUND_COMPILE_MODE_ADDITIVE:
        # update the flags, compression, encoding, and sample rate
        # of the tag to that of the samples being stored in it.
        tagdata.flags.fit_to_adpcm_blocksize = False
        tagdata.flags.split_long_sound_into_permutations = bool(
            blam_sound_bank.split_into_smaller_chunks)

        if blam_sound_bank.compression in (constants.COMPRESSION_PCM_16_LE,
                                           constants.COMPRESSION_PCM_16_BE):
            tagdata.compression.set_to("none")
        elif blam_sound_bank.compression == constants.COMPRESSION_ADPCM:
            tagdata.flags.fit_to_adpcm_blocksize = True
            tagdata.compression.set_to("xbox_adpcm")
        elif blam_sound_bank.compression == constants.COMPRESSION_OGG:
            tagdata.compression.set_to("ogg")
        else:
            errors.append('Unknown compression "%s"' %
                          blam_sound_bank.compression)

        if blam_sound_bank.encoding == constants.ENCODING_MONO:
            tagdata.encoding.set_to("mono")
        elif blam_sound_bank.encoding == constants.ENCODING_STEREO:
            tagdata.encoding.set_to("stereo")
        else:
            errors.append('Unknown encoding "%s"' %
                          blam_sound_bank.encoding)

        if blam_sound_bank.sample_rate == constants.SAMPLE_RATE_22K:
            tagdata.sample_rate.set_to("khz_22")
        elif blam_sound_bank.sample_rate == constants.SAMPLE_RATE_44K:
            tagdata.sample_rate.set_to("khz_44")
        else:
            errors.append('Unsupported sample rate "%s"' %
                          blam_sound_bank.sample_rate)

        if errors:
            return errors


    # make sure the encoding and sample rate of the
    # BlamSoundBank match the settings in the tagdata.
    snd__sample_rate = constants.halo_1_sample_rates.get(
        tagdata.sample_rate.data, "invalid")
    snd__channel_count = constants.channel_counts.get(
        tagdata.encoding.data, "invalid")
    blam_channel_count = constants.channel_counts.get(
        blam_sound_bank.encoding, "invalid")

    if snd__sample_rate != blam_sound_bank.sample_rate:
        errors.append('Cannot add %skHz sounds to %skHz tag.' %
                      (blam_sound_bank.sample_rate, snd__sample_rate))

    if snd__channel_count != blam_channel_count:
        errors.append('Cannot add %s channel sounds to %s channel tag.' %
                      (blam_channel_count, snd__channel_count))


    if errors:
        return errors

    snd__pitch_ranges = tagdata.pitch_ranges.STEPTREE
    blam_pitch_ranges = blam_sound_bank.pitch_ranges
    snd__pitch_ranges_by_name = {}
    prev_snd__pitch_ranges_by_name = {
        pr.name.lower().strip(): pr
        for pr in snd__pitch_ranges
        }

    encoding = tagdata.encoding.data
    sample_rate = constants.halo_1_sample_rates.get(
        tagdata.sample_rate.data, 0)

    # loop over the blam_sound_bank pitch ranges and compile them
    for blam_pr_name in sorted(blam_pitch_ranges):
        name = get_unique_name_31char(blam_pr_name.strip().lower(),
                                      snd__pitch_ranges_by_name)

        snd__pitch_ranges.append()  # create the new pitch range block
        snd__pitch_ranges_by_name[name], _ = snd__pitch_ranges.pop(-1)
        snd__pitch_ranges_by_name[name].name = name
        try:
            print("Compiling '%s'" % blam_pr_name)
            errors.extend(compile_pitch_range(
                snd__pitch_ranges_by_name[name],
                blam_pitch_ranges[blam_pr_name],
                snd__channel_count, snd__sample_rate, ignore_size_limits))
        except Exception:
            errors.append(traceback.format_exc())
            errors.append("Could not compile pitch range '%s'" % blam_pr_name)
            snd__pitch_ranges_by_name.pop(name)


    if update_mode != constants.SOUND_COMPILE_MODE_NEW:
        # preserve any old tag values and/or permutations
        for snd__pr_name, snd__pr in snd__pitch_ranges_by_name.items():
            prev_snd__pr = prev_snd__pitch_ranges_by_name.get(snd__pr_name)
            if prev_snd__pr is None:
                continue

            snd__pr.natural_pitch = prev_snd__pr.natural_pitch
            snd__pr.bend_bounds = prev_snd__pr.bend_bounds

            prev_perms = prev_snd__pr.permutations.STEPTREE
            perms = snd__pr.permutations.STEPTREE

            prev_perm_count = max(0, min(
                len(prev_perms), prev_snd__pr.actual_permutation_count))
            perm_count = max(0, min(
                len(perms), snd__pr.actual_permutation_count))

            # sort permutations by name so we can copy values
            perm_indices_by_name = {
                perm.name.strip().lower(): i
                for i, perm in enumerate(perms[: perm_count])
                }

            indices_to_merge = set()
            # copy values from old permutations into new ones
            for i, prev_perm in enumerate(prev_perms[: prev_perm_count]):
                perm_name = prev_perm.name.strip().lower()

                if perm_name not in perm_indices_by_name:
                    # no matching new perm. queue this one to be merged
                    indices_to_merge.add(i)
                    continue

                perm_pieces = get_permutation_chain(
                    perm_indices_by_name[perm_name], snd__pr)
                if not perm_pieces:
                    continue

                for perm_piece in perm_pieces:
                    perm_piece.name = prev_perm.name
                    perm_piece.gain = prev_perm.gain
                    perm_piece.skip_fraction = 0.0

                perm_pieces[0].skip_fraction = prev_perm.skip_fraction


            if update_mode != constants.SOUND_COMPILE_MODE_ADDITIVE:
                continue

            # merge old permutations into new pitch range
            for i in indices_to_merge:
                errors.extend(
                    merge_permutation_chain(
                        get_permutation_chain(i, prev_snd__pr),
                        snd__pr, ignore_size_limits)
                    )


    if update_mode == constants.SOUND_COMPILE_MODE_ADDITIVE:
        # add back in any pitch ranges missing from the old tag
        snd__pitch_ranges_by_name.update(
            {name: pr for name, pr in
             prev_snd__pitch_ranges_by_name.items()
             if name not in snd__pitch_ranges_by_name}
            )

    # clear the pitch ranges and update with the new ones
    del snd__pitch_ranges[:]
    for snd__pr_name in sorted(snd__pitch_ranges_by_name):
        pitch_range = snd__pitch_ranges_by_name[snd__pr_name]
        if not pitch_range.permutations.STEPTREE:
            continue

        if len(snd__pitch_ranges) < snd__pitch_ranges.MAX or ignore_size_limits:
            snd__pitch_ranges.append(pitch_range)
        else:
            errors.append("Too many pitch ranges. Cannot add '%s'" %
                          snd__pr_name)

    return errors


def get_unique_name_31char(name, names):
    name = name[: 31]
    if name not in names:
        return name

    i = 1
    end_str = ""
    while name[: 31 - len(end_str)] + end_str in names:
        end_str = "~" + str(i)
        i += 1

    return name[: 31 - len(end_str)] + end_str


def get_permutation_chain(start_index, pitch_range):
    seen = set()
    chain = []
    perms = pitch_range.permutations.STEPTREE
    i = start_index
    while i in range(len(perms)) and i not in seen:
        seen.add(i)
        chain.append(perms[i])
        i = perms[i].next_permutation_index

    return chain


def merge_permutation_chain(perm_chain, pitch_range, ignore_size_limits=False):
    errors = []
    if not perm_chain:
        return errors

    perms = pitch_range.permutations.STEPTREE
    perm_count = max(0, min(len(perms), pitch_range.actual_permutation_count))
    if ignore_size_limits:
        if perm_count + 1 >= 0x8000:
            errors.append("Too many permutations. Cannot add '%s'" %
                          perm_chain[0].name)
    elif len(perms) + len(perm_chain) > perms.MAX:
        errors.append("Too many permutation pieces. Cannot add '%s'" %
                      perm_chain[0].name)

    if errors:
        return errors

    for perm in perms:
        # shift all the next perm indices to account for the added perm
        if perm.next_permutation_index >= perm_count:
            perm.next_permutation_index += 1

    # insert the first piece of the permutation chain into the perms
    pitch_range.actual_permutation_count += 1
    perms.insert(perm_count, perm_chain[0])
    perm_chain[0].next_permutation_index = len(perms)

    # append and set the next index for each piece in the chain
    for perm in perm_chain[1: ]:
        perms.append(perm)
        perm.next_permutation_index = len(perms)

    # cut off the chain at last piece
    perm_chain[-1].next_permutation_index = -1

    return errors
